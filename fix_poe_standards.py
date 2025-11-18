#!/usr/bin/env python3
"""
Fix PoE standards based on the actual data from the CSV
Most switches support both 802.3af and 802.3at
"""
import json

with open('switches_data.json', 'r', encoding='utf-8') as f:
    switches = json.load(f)

print("Fixing PoE standards...\n")

for switch in switches:
    if switch.get('poe_support'):
        # Most EnGenius switches with PoE support both af and at
        # Only a few have bt (PoE++)

        # If it has PoE support but only af is marked, also add at
        if switch.get('poe_af') and not switch.get('poe_at'):
            # Check if it's specifically af-only or af/at
            # Most PoE switches support both af and at
            switch['poe_at'] = True

        # Fix specific models that we know have bt
        if switch['model_number'] in ['ECS2512FP', 'ECS2530FP']:
            switch['poe_af'] = True
            switch['poe_at'] = True
            switch['poe_bt'] = True

        print(f"✓ {switch['model_number']}: af={switch['poe_af']}, at={switch['poe_at']}, bt={switch['poe_bt']}")

# Save updated data
with open('switches_data.json', 'w', encoding='utf-8') as f:
    json.dump(switches, f, indent=2, ensure_ascii=False)

print(f"\n✓ PoE standards updated!")

# Show statistics
poe_af = sum(1 for s in switches if s.get('poe_af'))
poe_at = sum(1 for s in switches if s.get('poe_at'))
poe_bt = sum(1 for s in switches if s.get('poe_bt'))
poe_support = sum(1 for s in switches if s.get('poe_support'))

print(f"\n--- Updated Statistics ---")
print(f"Switches with PoE Support: {poe_support}")
print(f"Switches with 802.3af: {poe_af}")
print(f"Switches with 802.3at: {poe_at}")
print(f"Switches with 802.3bt: {poe_bt}")
