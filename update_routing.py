import json

# Leer el archivo JSON actual
with open('switches_data.json', 'r', encoding='utf-8') as f:
    switches = json.load(f)

# Modelos a actualizar
models_to_update = ['ECS5512', 'ECS5512FP']

# Contador de switches actualizados
updated_count = 0

# Actualizar los switches
for switch in switches:
    if switch['model_number'] in models_to_update:
        switch['dynamic_routing'] = True
        switch['layer'] = 'L3'  # Cambiar a L3 ya que tienen enrutamiento dinámico
        print(f"✓ Actualizado {switch['model_number']} - {switch['model_name']}")
        print(f"  - Enrutamiento dinámico: {switch['dynamic_routing']}")
        print(f"  - Capa: {switch['layer']}")
        print(f"  - Protocolos: RIP, OSPF\n")
        updated_count += 1

# Guardar el archivo actualizado
with open('switches_data.json', 'w', encoding='utf-8') as f:
    json.dump(switches, f, indent=2, ensure_ascii=False)

print(f"✓ Actualización completada!")
print(f"✓ Switches actualizados: {updated_count}")
print(f"✓ Total de switches en la base de datos: {len(switches)}")

# Mostrar resumen de switches con enrutamiento dinámico
dynamic_routing_switches = [s for s in switches if s['dynamic_routing']]
print(f"\nSwitches con enrutamiento dinámico (RIP/OSPF): {len(dynamic_routing_switches)}")
for s in dynamic_routing_switches:
    print(f"  - {s['model_number']}: {s['model_name']}")
