import json
import csv

# Leer el archivo JSON actual
with open('switches_data.json', 'r', encoding='utf-8') as f:
    switches = json.load(f)

# Leer datos adicionales del CSV
def get_additional_data_from_csv(model_number):
    """Obtiene datos adicionales del CSV para un modelo específico"""
    csv_file = 'EnGenius_Switch_Specs_ECS Switch.csv'

    additional_data = {
        'sdram': '',
        'flash_memory': '',
        'mac_address_table': '',
        'packet_buffer': '',
        'management_interfaces': [],
        'vlan_support': False,
        'qos_queues': '',
        'acl_support': False,
        'spanning_tree': [],
        'link_aggregation': False,
        'snmp_support': False,
        'operating_temp': '',
        'operating_humidity': '',
        'dimensions': '',
        'weight': '',
        'power_source': '',
        'form_factor_detail': ''
    }

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

            # Encontrar la columna del modelo
            model_col = -1
            if len(rows) > 1:
                for col_idx, cell in enumerate(rows[1]):
                    if cell == model_number:
                        model_col = col_idx
                        break

            if model_col == -1:
                return additional_data

            # Mapear filas a datos
            for idx, row in enumerate(rows):
                if len(row) > 0 and len(row) > model_col:
                    label = row[0].strip() if row[0] else ''
                    value = row[model_col].strip() if model_col < len(row) else ''

                    if not value or value == '-':
                        continue

                    # SDRAM
                    if label == 'SDRAM':
                        additional_data['sdram'] = value

                    # Flash Memory
                    elif label == 'Flash Memory':
                        additional_data['flash_memory'] = value

                    # MAC Address Table
                    elif 'MAC Address Table' in label:
                        additional_data['mac_address_table'] = value

                    # Packet Buffer
                    elif 'Packet Buffer' in label:
                        additional_data['packet_buffer'] = value

                    # Management
                    elif 'EnGenius Cloud' in value or 'Web GUI' in value:
                        if 'EnGenius Cloud' in value:
                            additional_data['management_interfaces'].append('EnGenius Cloud')
                        if 'Web GUI' in value or 'Local Web GUI' in value:
                            additional_data['management_interfaces'].append('Web GUI')
                        if 'SkyKey' in value:
                            additional_data['management_interfaces'].append('SkyKey')
                        if 'ezMaster' in value:
                            additional_data['management_interfaces'].append('ezMaster')

                    # VLAN
                    elif '802.1Q VLAN' in value or 'VLAN tagging' in value:
                        additional_data['vlan_support'] = True

                    # QoS
                    elif label == 'Queue' or 'Queue' in label:
                        additional_data['qos_queues'] = value

                    # ACL
                    elif 'ACL' in value and ('MAC Based' in value or 'IPv4' in value):
                        additional_data['acl_support'] = True

                    # Spanning Tree
                    elif 'Spanning Tree' in value:
                        if '802.1D' in value and '802.1D Spanning Tree' not in additional_data['spanning_tree']:
                            additional_data['spanning_tree'].append('802.1D STP')
                        if '802.1w' in value and '802.1w RSTP' not in additional_data['spanning_tree']:
                            additional_data['spanning_tree'].append('802.1w RSTP')
                        if '802.1S' in value and '802.1S MSTP' not in additional_data['spanning_tree']:
                            additional_data['spanning_tree'].append('802.1S MSTP')

                    # Link Aggregation
                    elif '802.3ad' in value or 'Link Aggregation' in value:
                        additional_data['link_aggregation'] = True

                    # SNMP
                    elif 'SNMP' in value:
                        additional_data['snmp_support'] = True

                    # Temperature
                    elif 'Operating:' in label and 'Temperature' not in label:
                        if '°F' in value or '°C' in value:
                            additional_data['operating_temp'] = value
                        elif '%' in value:
                            additional_data['operating_humidity'] = value

                    # Dimensions
                    elif 'Weight:' in value or 'Width:' in value:
                        additional_data['dimensions'] = value
                        if 'Weight:' in value:
                            import re
                            weight_match = re.search(r'Weight:\s*([^\\n]+)', value)
                            if weight_match:
                                additional_data['weight'] = weight_match.group(1).strip()

                    # Power Source
                    elif label == 'Power Source':
                        additional_data['power_source'] = value

    except FileNotFoundError:
        pass

    return additional_data

print("Enriqueciendo datos de switches con información adicional...\n")

# Actualizar cada switch con datos adicionales
for switch in switches:
    additional = get_additional_data_from_csv(switch['model_number'])

    # Agregar campos adicionales
    switch['sdram'] = additional['sdram']
    switch['flash_memory'] = additional['flash_memory']
    switch['mac_address_table'] = additional['mac_address_table']
    switch['packet_buffer'] = additional['packet_buffer']
    switch['management_interfaces'] = additional['management_interfaces']
    switch['vlan_support'] = additional['vlan_support']
    switch['qos_queues'] = additional['qos_queues']
    switch['acl_support'] = additional['acl_support']
    switch['spanning_tree'] = additional['spanning_tree']
    switch['link_aggregation'] = additional['link_aggregation']
    switch['snmp_support'] = additional['snmp_support']
    switch['operating_temp'] = additional['operating_temp']
    switch['operating_humidity'] = additional['operating_humidity']
    switch['dimensions'] = additional['dimensions']
    switch['weight'] = additional['weight']
    switch['power_source'] = additional['power_source']

    print(f"✓ {switch['model_number']}: Agregados {len([v for v in additional.values() if v])} campos adicionales")

# Guardar datos actualizados
with open('switches_data.json', 'w', encoding='utf-8') as f:
    json.dump(switches, f, indent=2, ensure_ascii=False)

print(f"\n✓ Datos enriquecidos guardados!")
print(f"✓ Total de switches: {len(switches)}")

# Mostrar ejemplo de un switch
print("\n--- Ejemplo de datos enriquecidos (primer switch) ---")
example = switches[0]
print(f"Modelo: {example['model_number']}")
print(f"SDRAM: {example.get('sdram', 'N/A')}")
print(f"Flash: {example.get('flash_memory', 'N/A')}")
print(f"MAC Table: {example.get('mac_address_table', 'N/A')}")
print(f"Management: {', '.join(example.get('management_interfaces', []))}")
print(f"VLAN: {example.get('vlan_support', False)}")
print(f"Spanning Tree: {', '.join(example.get('spanning_tree', []))}")
