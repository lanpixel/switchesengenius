import json

# Leer el archivo JSON actual
with open('switches_data.json', 'r', encoding='utf-8') as f:
    switches = json.load(f)

print("Completando características adicionales...\n")

# Para todos los switches gestionados CloudSwitch ECS, agregar características comunes
for switch in switches:
    model = switch['model_number']

    # Todos los switches CloudSwitch ECS tienen estas características
    if model.startswith('ECS'):
        # Spanning Tree - todos los ECS tienen STP/RSTP/MSTP
        if not switch.get('spanning_tree') or len(switch.get('spanning_tree', [])) == 0:
            switch['spanning_tree'] = ['802.1D STP', '802.1w RSTP', '802.1S MSTP']

        # Link Aggregation - todos los ECS lo tienen
        switch['link_aggregation'] = True

        # VLAN Support - todos lo tienen
        switch['vlan_support'] = True

        # SNMP - todos lo tienen
        switch['snmp_support'] = True

        # ACL - todos lo tienen
        switch['acl_support'] = True

    # FitSwitch también tienen características similares
    elif model.startswith('EWS'):
        if not switch.get('spanning_tree') or len(switch.get('spanning_tree', [])) == 0:
            switch['spanning_tree'] = ['802.1D STP', '802.1w RSTP']

        switch['link_aggregation'] = True
        switch['vlan_support'] = True
        switch['snmp_support'] = True
        switch['acl_support'] = True

        # Management para FitSwitch
        if not switch.get('management_interfaces') or len(switch.get('management_interfaces', [])) == 0:
            switch['management_interfaces'] = ['EnGenius Cloud', 'Web GUI', 'ezMaster']

        # Memoria para FitSwitch
        if not switch.get('sdram'):
            switch['sdram'] = '256MB'
        if not switch.get('flash_memory'):
            switch['flash_memory'] = '32MB'

        # QoS
        if not switch.get('qos_queues'):
            switch['qos_queues'] = 'Queue 8'

    print(f"✓ {model}: Características completadas")

# Guardar datos actualizados
with open('switches_data.json', 'w', encoding='utf-8') as f:
    json.dump(switches, f, indent=2, ensure_ascii=False)

print(f"\n✓ Características completadas!")
print(f"✓ Total de switches: {len(switches)}")

# Mostrar estadísticas
print("\n--- Estadísticas ---")
print(f"Switches con VLAN: {sum(1 for s in switches if s.get('vlan_support'))}")
print(f"Switches con Spanning Tree: {sum(1 for s in switches if s.get('spanning_tree') and len(s.get('spanning_tree', [])) > 0)}")
print(f"Switches con Link Aggregation: {sum(1 for s in switches if s.get('link_aggregation'))}")
print(f"Switches con ACL: {sum(1 for s in switches if s.get('acl_support'))}")
print(f"Switches con SNMP: {sum(1 for s in switches if s.get('snmp_support'))}")
print(f"Switches con interfaces de gestión: {sum(1 for s in switches if s.get('management_interfaces') and len(s.get('management_interfaces', [])) > 0)}")
