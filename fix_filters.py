#!/usr/bin/env python3
"""
Fix the applyFilters function to handle missing elements gracefully
"""

with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the applyFilters function with a safer version
old_apply_filters = """// Apply all active filters
function applyFilters() {
    const filters = {
        // Port filters
        gigabit: document.getElementById('filter-gigabit').checked,
        minGigabit: parseInt(document.getElementById('min-gigabit').value) || 0,

        multigig: document.getElementById('filter-multigig').checked,
        minMultigig: parseInt(document.getElementById('min-multigig').value) || 0,

        tenGig: document.getElementById('filter-10gig').checked,
        minTenGig: parseInt(document.getElementById('min-10gig').value) || 0,

        sfp: document.getElementById('filter-sfp').checked,
        minSfp: parseInt(document.getElementById('min-sfp').value) || 0,

        sfpPlus: document.getElementById('filter-sfp-plus').checked,
        minSfpPlus: parseInt(document.getElementById('min-sfp-plus').value) || 0,

        // PoE filters
        poe: document.getElementById('filter-poe').checked,
        poeAf: document.getElementById('filter-poe-af').checked,
        poeAt: document.getElementById('filter-poe-at').checked,
        poeBt: document.getElementById('filter-poe-bt').checked,
        minPoeBudget: parseInt(document.getElementById('min-poe-budget').value) || 0,

        // Management filters
        managed: document.getElementById('filter-managed').checked,
        dhcpSnooping: document.getElementById('filter-dhcp-snooping').checked,
        igmpSnooping: document.getElementById('filter-igmp-snooping').checked,

        // Layer filters
        l2: document.getElementById('filter-l2').checked,
        staticRouting: document.getElementById('filter-static-routing').checked,
        dynamicRouting: document.getElementById('filter-dynamic-routing').checked,
    };"""

new_apply_filters = """// Helper function to safely get element value
function getElementValue(id, isCheckbox = false) {
    const el = document.getElementById(id);
    if (!el) return isCheckbox ? false : 0;
    return isCheckbox ? el.checked : (parseInt(el.value) || 0);
}

// Apply all active filters
function applyFilters() {
    const filters = {
        // Port filters
        gigabit: getElementValue('filter-gigabit', true),
        minGigabit: getElementValue('min-gigabit'),

        multigig: getElementValue('filter-multigig', true),
        minMultigig: getElementValue('min-multigig'),

        tenGig: getElementValue('filter-10gig', true),
        minTenGig: getElementValue('min-10gig'),

        sfp: getElementValue('filter-sfp', true),
        minSfp: getElementValue('min-sfp'),

        sfpPlus: getElementValue('filter-sfp-plus', true),
        minSfpPlus: getElementValue('min-sfp-plus'),

        // PoE filters
        poe: getElementValue('filter-poe', true),
        poeAf: getElementValue('filter-poe-af', true),
        poeAt: getElementValue('filter-poe-at', true),
        poeBt: getElementValue('filter-poe-bt', true),
        minPoeBudget: getElementValue('min-poe-budget'),

        // Management filters
        managed: getElementValue('filter-managed', true),
        dhcpSnooping: getElementValue('filter-dhcp-snooping', true),
        igmpSnooping: getElementValue('filter-igmp-snooping', true),

        // Layer filters
        l2: getElementValue('filter-l2', true),
        staticRouting: getElementValue('filter-static-routing', true),
        dynamicRouting: getElementValue('filter-dynamic-routing', true),
    };"""

content = content.replace(old_apply_filters, new_apply_filters)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed applyFilters function to handle missing elements")
print("✓ Filters should now work correctly")
print("✓ Reload http://localhost:8080 to test")
