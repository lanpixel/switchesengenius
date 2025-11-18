#!/usr/bin/env python3
"""
Fix layer classification
L3 should only be for switches with dynamic routing (RIP/OSPF)
L2+ is for advanced L2 switches with static routing
"""
import json

with open('switches_data.json', 'r', encoding='utf-8') as f:
    switches = json.load(f)

print("Fixing layer classification...\n")

for switch in switches:
    old_layer = switch['layer']

    # Only switches with dynamic_routing should be L3
    if switch.get('dynamic_routing'):
        switch['layer'] = 'L3'
    # Switches with static routing but no dynamic routing are L2+
    elif switch.get('static_routing'):
        switch['layer'] = 'L2+'
    # Basic switches are L2
    else:
        switch['layer'] = 'L2'

    if old_layer != switch['layer']:
        print(f"✓ {switch['model_number']}: {old_layer} → {switch['layer']}")

# Save updated data
with open('switches_data.json', 'w', encoding='utf-8') as f:
    json.dump(switches, f, indent=2, ensure_ascii=False)

print(f"\n✓ Layer classification updated!")

# Show statistics
l2 = sum(1 for s in switches if s['layer'] == 'L2')
l2_plus = sum(1 for s in switches if s['layer'] == 'L2+')
l3 = sum(1 for s in switches if s['layer'] == 'L3')

print(f"\n--- Updated Distribution ---")
print(f"L2 switches: {l2}")
print(f"L2+ switches: {l2_plus}")
print(f"L3 switches (with dynamic routing): {l3}")
print()
print("L3 switches:")
for s in switches:
    if s['layer'] == 'L3':
        print(f"  - {s['model_number']}: {s['model_name']}")
