import json

# Leer el archivo JSON actual
with open('switches_data.json', 'r', encoding='utf-8') as f:
    switches = json.load(f)

# Nuevo switch a agregar
new_switch = {
    "model_name": "CloudSwitch MGPlus 24 Full PoE 6 SFP+",
    "model_number": "ECS2530FP",
    "gigabit_ports": 0,
    "multi_gigabit_ports": 24,  # 24x 100/1000/2500 Mbps Ports
    "sfp_ports": 0,
    "sfp_plus_ports": 6,  # 6x SFP+ Ports
    "ten_gig_ports": 0,
    "poe_support": True,
    "poe_af": True,  # 802.3af
    "poe_at": True,  # 802.3at
    "poe_bt": True,  # 802.3bt
    "poe_budget": 740,  # 740W
    "managed": True,
    "layer": "L2+",
    "dhcp_relay": True,  # IPv4 DHCP Relay presente en las especificaciones
    "dhcp_snooping": True,  # IPv4 DHCP Snooping presente
    "igmp_snooping": True,  # IGMP Snooping presente
    "static_routing": True,  # L2+ incluye características L3 básicas
    "dynamic_routing": False,
    "switching_capacity": "192Gbps",
    "form_factor": "19\" 1U",
    "power_consumption": ""
}

# Agregar el nuevo switch
switches.append(new_switch)

# Guardar el archivo actualizado
with open('switches_data.json', 'w', encoding='utf-8') as f:
    json.dump(switches, f, indent=2, ensure_ascii=False)

print(f"✓ Switch {new_switch['model_number']} agregado exitosamente!")
print(f"✓ Total de switches ahora: {len(switches)}")
print(f"\nDetalles del switch agregado:")
print(f"  Modelo: {new_switch['model_name']}")
print(f"  Número: {new_switch['model_number']}")
print(f"  Puertos Multi-Gigabit: {new_switch['multi_gigabit_ports']}")
print(f"  Puertos SFP+: {new_switch['sfp_plus_ports']}")
print(f"  PoE Budget: {new_switch['poe_budget']}W")
print(f"  PoE: af/at/bt: {new_switch['poe_af']}/{new_switch['poe_at']}/{new_switch['poe_bt']}")
print(f"  Switching Capacity: {new_switch['switching_capacity']}")
print(f"  DHCP Snooping: {new_switch['dhcp_snooping']}")
print(f"  IGMP Snooping: {new_switch['igmp_snooping']}")
