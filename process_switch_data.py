import csv
import json
import re

def extract_number(text):
    """Extrae números de una cadena de texto"""
    if not text or text == '-':
        return 0
    match = re.search(r'(\d+)', str(text))
    return int(match.group(1)) if match else 0

def extract_poe_budget(text):
    """Extrae el presupuesto PoE en watts"""
    if not text or text == '-':
        return 0
    match = re.search(r'(\d+)\s*[Ww]', str(text))
    return int(match.group(1)) if match else 0

def has_feature(text):
    """Verifica si una característica está presente"""
    if not text or text == '-' or text == '':
        return False
    return True

def process_csv_data(csv_file):
    """Procesa un archivo CSV y extrae información de switches"""
    switches = []

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

        if len(rows) < 2:
            return switches

        # Encontrar índices de filas importantes
        model_name_row = 0
        model_number_row = 1

        # Crear un diccionario para mapear nombres de filas a índices
        row_map = {}
        for idx, row in enumerate(rows):
            if row and row[0]:
                row_map[row[0].strip()] = idx

        # Número de modelos (columnas) excluyendo la primera columna
        num_models = len(rows[0]) - 1

        # Procesar cada modelo
        for col_idx in range(1, num_models + 1):
            if col_idx >= len(rows[model_name_row]):
                continue

            model_name = rows[model_name_row][col_idx] if col_idx < len(rows[model_name_row]) else ''
            model_number = rows[model_number_row][col_idx] if col_idx < len(rows[model_number_row]) else ''

            # Saltar columnas vacías
            if not model_name and not model_number:
                continue

            switch = {
                'model_name': model_name,
                'model_number': model_number,
                'gigabit_ports': 0,
                'multi_gigabit_ports': 0,
                'sfp_ports': 0,
                'sfp_plus_ports': 0,
                'ten_gig_ports': 0,
                'poe_support': False,
                'poe_af': False,
                'poe_at': False,
                'poe_bt': False,
                'poe_budget': 0,
                'managed': True,  # Asumimos que todos los CloudSwitch/FitSwitch son gestionados
                'layer': 'L2',
                'dhcp_relay': False,
                'dhcp_snooping': False,
                'igmp_snooping': False,
                'static_routing': False,
                'dynamic_routing': False,
                'switching_capacity': '',
                'form_factor': '',
                'power_consumption': ''
            }

            # Extraer puertos Gigabit
            gigabit_key = 'Network Port  -\nGigabit Ethernet Ports'
            gigabit_key_alt = 'Network Port -\nGigabit Ethernet Ports'
            if gigabit_key in row_map:
                gigabit_text = rows[row_map[gigabit_key]][col_idx] if col_idx < len(rows[row_map[gigabit_key]]) else ''
                switch['gigabit_ports'] = extract_number(gigabit_text)
            elif gigabit_key_alt in row_map:
                gigabit_text = rows[row_map[gigabit_key_alt]][col_idx] if col_idx < len(rows[row_map[gigabit_key_alt]]) else ''
                switch['gigabit_ports'] = extract_number(gigabit_text)

            # Extraer puertos Multi-Gigabit
            multi_gig_key = 'Network Port - \nMulti-Gigabit Ethernet Ports'
            if multi_gig_key in row_map:
                multi_gig_text = rows[row_map[multi_gig_key]][col_idx] if col_idx < len(rows[row_map[multi_gig_key]]) else ''
                switch['multi_gigabit_ports'] = extract_number(multi_gig_text)

                # Detectar puertos 10G basado en el texto
                if multi_gig_text and '10000' in multi_gig_text or '10G' in multi_gig_text:
                    switch['ten_gig_ports'] = extract_number(multi_gig_text)

            # Extraer puertos SFP
            sfp_key = 'Network Port - \nSFP Ports'
            if sfp_key in row_map:
                sfp_text = rows[row_map[sfp_key]][col_idx] if col_idx < len(rows[row_map[sfp_key]]) else ''
                switch['sfp_ports'] = extract_number(sfp_text)

            # Extraer puertos SFP+
            sfp_plus_key = 'Network Port - \nSFP+ Ports/'
            if sfp_plus_key in row_map:
                sfp_plus_text = rows[row_map[sfp_plus_key]][col_idx] if col_idx < len(rows[row_map[sfp_plus_key]]) else ''
                switch['sfp_plus_ports'] = extract_number(sfp_plus_text)

            # Extraer información PoE
            poe_key = 'PoE Capable Ports'
            if poe_key in row_map:
                poe_text = rows[row_map[poe_key]][col_idx] if col_idx < len(rows[row_map[poe_key]]) else ''
                if poe_text and poe_text != '-':
                    switch['poe_support'] = True
                    if '802.3af' in poe_text:
                        switch['poe_af'] = True
                    if '802.3at' in poe_text:
                        switch['poe_at'] = True
                    if '802.3bt' in poe_text or 'bt' in poe_text:
                        switch['poe_bt'] = True

            # Extraer presupuesto PoE
            poe_budget_key = 'Total PoE Budget'
            if poe_budget_key in row_map:
                poe_budget_text = rows[row_map[poe_budget_key]][col_idx] if col_idx < len(rows[row_map[poe_budget_key]]) else ''
                switch['poe_budget'] = extract_poe_budget(poe_budget_text)

            # Buscar características L3 y L2
            for idx, row in enumerate(rows):
                if not row or not row[0]:
                    continue

                feature_name = row[0].strip()
                feature_value = row[col_idx] if col_idx < len(row) else ''

                # DHCP Relay
                if 'IPv4 DHCP Relay' in feature_name or 'DHCP Relay' in feature_name:
                    switch['dhcp_relay'] = has_feature(feature_value)

                # DHCP Snooping
                if 'IPv4 DHCP Snooping' == feature_name or 'DHCP Snooping' in feature_name:
                    switch['dhcp_snooping'] = has_feature(feature_value)

                # IGMP Snooping
                if 'IGMP Snooping' == feature_name:
                    switch['igmp_snooping'] = has_feature(feature_value)

                # Static Routing
                if 'Static Route' in feature_name or 'IPv4 Static Routing' in feature_name:
                    switch['static_routing'] = has_feature(feature_value)
                    if has_feature(feature_value):
                        switch['layer'] = 'L3'

                # Dynamic Routing
                if any(proto in feature_name for proto in ['RIP', 'OSPF', 'BGP']):
                    if has_feature(feature_value):
                        switch['dynamic_routing'] = True
                        switch['layer'] = 'L3'

            # Determinar capa basado en el nombre del modelo
            if 'L2Plus' in model_name or 'L2+' in model_name:
                switch['layer'] = 'L2+'

            # Extraer capacidad de switching
            switching_key = 'Switching Capacity'
            if switching_key in row_map:
                switching_text = rows[row_map[switching_key]][col_idx] if col_idx < len(rows[row_map[switching_key]]) else ''
                switch['switching_capacity'] = switching_text if switching_text != '-' else ''

            # Solo agregar switches con información válida
            if switch['model_number']:
                switches.append(switch)

    return switches

# Procesar todos los archivos CSV
all_switches = []

print("Procesando archivos CSV...")

# Procesar ECS Switch
print("\nProcesando ECS Switch...")
ecs_switches = process_csv_data('EnGenius_Switch_Specs_ECS Switch.csv')
all_switches.extend(ecs_switches)
print(f"  Encontrados {len(ecs_switches)} switches ECS")

# Procesar Fit Switch
print("\nProcesando Fit Switch...")
fit_switches = process_csv_data('EnGenius_Switch_Specs_Fit Switch.csv')
all_switches.extend(fit_switches)
print(f"  Encontrados {len(fit_switches)} switches Fit")

# Guardar en JSON
output_file = 'switches_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_switches, f, indent=2, ensure_ascii=False)

print(f"\n✓ Procesamiento completado!")
print(f"✓ Total de switches procesados: {len(all_switches)}")
print(f"✓ Datos guardados en: {output_file}")

# Mostrar resumen de características
print("\n--- Resumen de características ---")
print(f"Switches con PoE: {sum(1 for s in all_switches if s['poe_support'])}")
print(f"Switches con Multi-Gigabit: {sum(1 for s in all_switches if s['multi_gigabit_ports'] > 0)}")
print(f"Switches con SFP+: {sum(1 for s in all_switches if s['sfp_plus_ports'] > 0)}")
print(f"Switches con IGMP Snooping: {sum(1 for s in all_switches if s['igmp_snooping'])}")
print(f"Switches con DHCP Snooping: {sum(1 for s in all_switches if s['dhcp_snooping'])}")
print(f"Switches con Static Routing: {sum(1 for s in all_switches if s['static_routing'])}")
