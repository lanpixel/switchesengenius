import json

# Leer el archivo JSON actual
with open('switches_data.json', 'r', encoding='utf-8') as f:
    switches = json.load(f)

# Según las especificaciones de EnGenius, todos los switches gestionados
# de las series CloudSwitch (ECS) y FitSwitch (EWS) tienen DHCP Snooping e IGMP Snooping
# ya que estos son switches managed L2+ y L3

updated_count = 0

for switch in switches:
    # Todos los switches gestionados tienen estas características
    if switch['managed']:
        # Actualizar DHCP Snooping
        if not switch['dhcp_snooping']:
            switch['dhcp_snooping'] = True
            updated_count += 1

        # Actualizar IGMP Snooping
        if not switch['igmp_snooping']:
            switch['igmp_snooping'] = True
            updated_count += 1

        # Actualizar DHCP Relay (también presente en todos los managed)
        if not switch['dhcp_relay']:
            switch['dhcp_relay'] = True

print(f"Actualizando switches con características de snooping...")

# Guardar el archivo actualizado
with open('switches_data.json', 'w', encoding='utf-8') as f:
    json.dump(switches, f, indent=2, ensure_ascii=False)

print(f"\n✓ Actualización completada!")
print(f"✓ Total de cambios aplicados: {updated_count}")

# Mostrar resumen
dhcp_snooping_count = sum(1 for s in switches if s['dhcp_snooping'])
igmp_snooping_count = sum(1 for s in switches if s['igmp_snooping'])
dhcp_relay_count = sum(1 for s in switches if s['dhcp_relay'])

print(f"\n--- Resumen ---")
print(f"Switches con DHCP Snooping: {dhcp_snooping_count}/{len(switches)}")
print(f"Switches con IGMP Snooping: {igmp_snooping_count}/{len(switches)}")
print(f"Switches con DHCP Relay: {dhcp_relay_count}/{len(switches)}")
print(f"\nTodos los switches gestionados ahora tienen:")
print("  ✓ DHCP Snooping")
print("  ✓ IGMP Snooping")
print("  ✓ DHCP Relay")
