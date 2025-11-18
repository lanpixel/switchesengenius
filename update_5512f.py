import json

# Leer el archivo JSON actual
with open('switches_data.json', 'r', encoding='utf-8') as f:
    switches = json.load(f)

# Encontrar y actualizar el ECS5512F
updated = False

for switch in switches:
    if switch['model_number'] == 'ECS5512F':
        switch['dynamic_routing'] = True
        switch['layer'] = 'L3'  # Cambiar a L3 ya que tiene enrutamiento dinámico

        print(f"✓ Actualizado {switch['model_number']} - {switch['model_name']}")
        print(f"  - Enrutamiento dinámico: {switch['dynamic_routing']}")
        print(f"  - Capa: {switch['layer']}")
        print(f"  - Protocolos: OSPF")
        print(f"  - Puertos SFP+: {switch['sfp_plus_ports']}")
        print(f"  - Capacidad: {switch['switching_capacity']}")
        updated = True
        break

if not updated:
    print("⚠️  No se encontró el switch ECS5512F")
else:
    # Guardar el archivo actualizado
    with open('switches_data.json', 'w', encoding='utf-8') as f:
        json.dump(switches, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Actualización completada!")

    # Mostrar resumen de switches con enrutamiento dinámico
    dynamic_routing_switches = [s for s in switches if s['dynamic_routing']]
    print(f"\nSwitches con enrutamiento dinámico (RIP/OSPF): {len(dynamic_routing_switches)}")
    for s in dynamic_routing_switches:
        print(f"  - {s['model_number']}: {s['model_name']} ({s['layer']})")
