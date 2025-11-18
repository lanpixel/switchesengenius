// Global variable to store all switches data
let allSwitches = [];
let filteredSwitches = [];

// Load switches data from JSON
async function loadSwitchesData() {
    try {
        const response = await fetch('switches_data.json');
        allSwitches = await response.json();
        filteredSwitches = [...allSwitches];
        displaySwitches(filteredSwitches);
        updateResultsCount(filteredSwitches.length);
    } catch (error) {
        console.error('Error loading switches data:', error);
        document.getElementById('results-container').innerHTML = `
            <div class="no-results">
                <div class="no-results-icon">⚠️</div>
                <h3>Error al cargar los datos</h3>
                <p>No se pudieron cargar los switches. Por favor, recarga la página.</p>
            </div>
        `;
    }
}

// Helper function to safely get element value
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
    };

    filteredSwitches = allSwitches.filter(sw => {
        // Port filters
        if (filters.gigabit && sw.gigabit_ports < filters.minGigabit) return false;
        if (filters.multigig && sw.multi_gigabit_ports < filters.minMultigig) return false;
        if (filters.tenGig && sw.ten_gig_ports < filters.minTenGig) return false;
        if (filters.sfp && sw.sfp_ports < filters.minSfp) return false;
        if (filters.sfpPlus && sw.sfp_plus_ports < filters.minSfpPlus) return false;

        // PoE filters
        if (filters.poe && !sw.poe_support) return false;
        if (filters.poeAf && !sw.poe_af) return false;
        if (filters.poeAt && !sw.poe_at) return false;
        if (filters.poeBt && !sw.poe_bt) return false;
        if (filters.minPoeBudget > 0 && sw.poe_budget < filters.minPoeBudget) return false;

        // Management filters
        if (filters.managed && !sw.managed) return false;
        if (filters.dhcpSnooping && !sw.dhcp_snooping) return false;
        if (filters.igmpSnooping && !sw.igmp_snooping) return false;

        // Layer filters
        if (filters.l2 && !sw.layer.includes('L2')) return false;
        if (filters.staticRouting && !sw.static_routing) return false;
        if (filters.dynamicRouting && !sw.dynamic_routing) return false;

        return true;
    });

    displaySwitches(filteredSwitches);
    updateResultsCount(filteredSwitches.length);
}

// Display switches in the results container
function displaySwitches(switches) {
    const container = document.getElementById('results-container');

    if (switches.length === 0) {
        container.innerHTML = `
            <div class="no-results">
                <div class="no-results-icon">🔍</div>
                <h3>No switches found</h3>
                <p>Try adjusting the filters to see more results</p>
            </div>
        `;
        return;
    }

    container.innerHTML = switches.map(sw => createSwitchCard(sw)).join('');
}

// Open modal with switch details
function openModal(switchData) {
    const modal = document.getElementById('modal-overlay');
    const title = document.getElementById('modal-title');
    const subtitle = document.getElementById('modal-subtitle');
    const body = document.getElementById('modal-body');

    title.textContent = switchData.model_name;
    subtitle.textContent = switchData.model_number;

    // Generate modal content
    body.innerHTML = generateModalContent(switchData);

    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Close modal
function closeModal() {
    const modal = document.getElementById('modal-overlay');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Close modal when clicking on overlay
function closeModalOnOverlay(event) {
    if (event.target.id === 'modal-overlay') {
        closeModal();
    }
}

// Generate modal content with all switch details
function generateModalContent(sw) {
    const poeStandards = [];
    if (sw.poe_af) poeStandards.push('802.3af');
    if (sw.poe_at) poeStandards.push('802.3at');
    if (sw.poe_bt) poeStandards.push('802.3bt');

    return `
        <!-- Badges -->
        <div style="margin-bottom: 20px;">
            <span class="modal-badge">${sw.layer}</span>
            ${sw.managed ? '<span class="modal-badge success">Managed</span>' : ''}
            ${sw.poe_support ? '<span class="modal-badge success">PoE</span>' : ''}
            ${sw.dynamic_routing ? '<span class="modal-badge success">L3 Dinámico</span>' : ''}
        </div>

        <!-- Puertos -->
        <div class="modal-section">
            <h3>🔌 Port Configuration</h3>
            <div class="modal-grid">
                ${sw.gigabit_ports > 0 ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">Gigabit Ethernet Ports</div>
                        <div class="modal-detail-value">${sw.gigabit_ports} ports</div>
                    </div>
                ` : ''}
                ${sw.multi_gigabit_ports > 0 ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">Multi-Gigabit Ports (2.5G/5G)</div>
                        <div class="modal-detail-value">${sw.multi_gigabit_ports} ports</div>
                    </div>
                ` : ''}
                ${sw.ten_gig_ports > 0 ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">10 Gigabit Ports</div>
                        <div class="modal-detail-value">${sw.ten_gig_ports} ports</div>
                    </div>
                ` : ''}
                ${sw.sfp_ports > 0 ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">SFP Ports</div>
                        <div class="modal-detail-value">${sw.sfp_ports} ports</div>
                    </div>
                ` : ''}
                ${sw.sfp_plus_ports > 0 ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">SFP Ports+</div>
                        <div class="modal-detail-value">${sw.sfp_plus_ports} ports</div>
                    </div>
                ` : ''}
            </div>
        </div>

        <!-- PoE -->
        ${sw.poe_support ? `
            <div class="modal-section">
                <h3>⚡ Power over Ethernet (PoE)</h3>
                <div class="modal-grid">
                    <div class="modal-detail">
                        <div class="modal-detail-label">PoE Standards</div>
                        <div class="modal-detail-value">${poeStandards.join(', ')}</div>
                    </div>
                    <div class="modal-detail">
                        <div class="modal-detail-label">Budget Total PoE</div>
                        <div class="modal-detail-value">${sw.poe_budget}W</div>
                    </div>
                </div>
            </div>
        ` : ''}

        <!-- Performance -->
        <div class="modal-section">
            <h3>💨 Performance</h3>
            <div class="modal-grid">
                ${sw.switching_capacity ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">Switching Capacity</div>
                        <div class="modal-detail-value">${sw.switching_capacity}</div>
                    </div>
                ` : ''}
                <div class="modal-detail">
                    <div class="modal-detail-label">Network Layer</div>
                    <div class="modal-detail-value">${sw.layer}</div>
                </div>
            </div>
        </div>

        <!-- Features de Red -->
        <div class="modal-section">
            <h3>🌐 Features de Red</h3>
            <div class="feature-list">
                <div class="feature-item ${sw.managed ? 'active' : 'inactive'}">
                    <span class="feature-icon">${sw.managed ? '✓' : '✗'}</span>
                    <span>Switch Managed</span>
                </div>
                <div class="feature-item ${sw.dhcp_relay ? 'active' : 'inactive'}">
                    <span class="feature-icon">${sw.dhcp_relay ? '✓' : '✗'}</span>
                    <span>DHCP Relay</span>
                </div>
                <div class="feature-item ${sw.dhcp_snooping ? 'active' : 'inactive'}">
                    <span class="feature-icon">${sw.dhcp_snooping ? '✓' : '✗'}</span>
                    <span>DHCP Snooping</span>
                </div>
                <div class="feature-item ${sw.igmp_snooping ? 'active' : 'inactive'}">
                    <span class="feature-icon">${sw.igmp_snooping ? '✓' : '✗'}</span>
                    <span>IGMP Snooping</span>
                </div>
                <div class="feature-item ${sw.static_routing ? 'active' : 'inactive'}">
                    <span class="feature-icon">${sw.static_routing ? '✓' : '✗'}</span>
                    <span>Static Routing L3</span>
                </div>
                <div class="feature-item ${sw.dynamic_routing ? 'active' : 'inactive'}">
                    <span class="feature-icon">${sw.dynamic_routing ? '✓' : '✗'}</span>
                    <span>Dynamic Routing (RIP/OSPF)</span>
                </div>
            </div>
        </div>

        <!-- Hardware -->
        <div class="modal-section">
            <h3>💾 Hardware</h3>
            <div class="modal-grid">
                ${sw.sdram ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">SDRAM</div>
                        <div class="modal-detail-value">${sw.sdram}</div>
                    </div>
                ` : ''}
                ${sw.flash_memory ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">Flash Memory</div>
                        <div class="modal-detail-value">${sw.flash_memory}</div>
                    </div>
                ` : ''}
                ${sw.mac_address_table ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">MAC Address Table</div>
                        <div class="modal-detail-value">${sw.mac_address_table}</div>
                    </div>
                ` : ''}
                ${sw.packet_buffer ? `
                    <div class="modal-detail">
                        <div class="modal-detail-label">Packet Buffer</div>
                        <div class="modal-detail-value">${sw.packet_buffer}</div>
                    </div>
                ` : ''}
            </div>
        </div>

        <!-- Gestión -->
        ${sw.management_interfaces && sw.management_interfaces.length > 0 ? `
            <div class="modal-section">
                <h3>🖥️ Management Interfaces</h3>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                    ${sw.management_interfaces.map(iface => `
                        <span class="modal-badge success">${iface}</span>
                    `).join('')}
                </div>
            </div>
        ` : ''}

        <!-- Features Avanzadas L2 -->
        <div class="modal-section">
            <h3>🔧 Features L2 Avanzadas</h3>
            <div class="feature-list">
                ${sw.vlan_support ? `
                    <div class="feature-item active">
                        <span class="feature-icon">✓</span>
                        <span>802.1Q VLAN</span>
                    </div>
                ` : ''}
                ${sw.spanning_tree && sw.spanning_tree.length > 0 ?
                    sw.spanning_tree.map(stp => `
                        <div class="feature-item active">
                            <span class="feature-icon">✓</span>
                            <span>${stp}</span>
                        </div>
                    `).join('') : ''
                }
                ${sw.link_aggregation ? `
                    <div class="feature-item active">
                        <span class="feature-icon">✓</span>
                        <span>802.3ad Link Aggregation</span>
                    </div>
                ` : ''}
                ${sw.qos_queues ? `
                    <div class="feature-item active">
                        <span class="feature-icon">✓</span>
                        <span>QoS (${sw.qos_queues} Queues)</span>
                    </div>
                ` : ''}
            </div>
        </div>

        <!-- Security -->
        <div class="modal-section">
            <h3>🔒 Security</h3>
            <div class="feature-list">
                ${sw.acl_support ? `
                    <div class="feature-item active">
                        <span class="feature-icon">✓</span>
                        <span>Access Control Lists (ACL)</span>
                    </div>
                ` : ''}
                <div class="feature-item ${sw.dhcp_snooping ? 'active' : 'inactive'}">
                    <span class="feature-icon">${sw.dhcp_snooping ? '✓' : '✗'}</span>
                    <span>DHCP Snooping</span>
                </div>
                ${sw.snmp_support ? `
                    <div class="feature-item active">
                        <span class="feature-icon">✓</span>
                        <span>SNMP v1/v2c/v3</span>
                    </div>
                ` : ''}
            </div>
        </div>

        <!-- Physical Specifications -->
        ${sw.power_source || sw.operating_temp || sw.dimensions ? `
            <div class="modal-section">
                <h3>📐 Physical Specifications</h3>
                <div class="modal-grid">
                    ${sw.power_source ? `
                        <div class="modal-detail">
                            <div class="modal-detail-label">Power Source</div>
                            <div class="modal-detail-value">${sw.power_source}</div>
                        </div>
                    ` : ''}
                    ${sw.operating_temp ? `
                        <div class="modal-detail">
                            <div class="modal-detail-label">Operating Temperature</div>
                            <div class="modal-detail-value">${sw.operating_temp}</div>
                        </div>
                    ` : ''}
                    ${sw.operating_humidity ? `
                        <div class="modal-detail">
                            <div class="modal-detail-label">Operating Humidity</div>
                            <div class="modal-detail-value">${sw.operating_humidity}</div>
                        </div>
                    ` : ''}
                    ${sw.dimensions ? `
                        <div class="modal-detail">
                            <div class="modal-detail-label">Dimensions</div>
                            <div class="modal-detail-value">${sw.dimensions}</div>
                        </div>
                    ` : ''}
                    ${sw.weight ? `
                        <div class="modal-detail">
                            <div class="modal-detail-label">Weight</div>
                            <div class="modal-detail-value">${sw.weight}</div>
                        </div>
                    ` : ''}
                </div>
            </div>
        ` : ''}

        <!-- Total Ports Summary -->
        <div class="modal-section">
            <h3>📊 Total Ports Summary</h3>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <div style="font-size: 2em; font-weight: bold; color: #667eea; margin-bottom: 10px;">
                    ${sw.gigabit_ports + sw.multi_gigabit_ports + sw.ten_gig_ports + sw.sfp_ports + sw.sfp_plus_ports} ports totales
                </div>
                <div style="color: #666;">
                    ${sw.gigabit_ports > 0 ? `${sw.gigabit_ports} Gigabit` : ''}
                    ${sw.multi_gigabit_ports > 0 ? ` + ${sw.multi_gigabit_ports} Multi-Gig` : ''}
                    ${sw.ten_gig_ports > 0 ? ` + ${sw.ten_gig_ports} 10G` : ''}
                    ${sw.sfp_ports > 0 ? ` + ${sw.sfp_ports} SFP` : ''}
                    ${sw.sfp_plus_ports > 0 ? ` + ${sw.sfp_plus_ports} SFP+` : ''}
                </div>
            </div>
        </div>
    `;
}

// Create HTML for a single switch card
function createSwitchCard(sw) {
    const poeStandards = [];
    if (sw.poe_af) poeStandards.push('802.3af');
    if (sw.poe_at) poeStandards.push('802.3at');
    if (sw.poe_bt) poeStandards.push('802.3bt');
    const poeText = poeStandards.length > 0 ? poeStandards.join(', ') : 'No';

    return `
        <div class="switch-card" onclick='openModal(${JSON.stringify(sw).replace(/'/g, "&#39;")})'>
            <div class="switch-header">
                <div class="switch-title">
                    <h3>${sw.model_name}</h3>
                    <p>${sw.model_number}</p>
                </div>
                <div class="switch-badge">${sw.layer}</div>
            </div>

            <div class="switch-specs">
                ${sw.gigabit_ports > 0 ? `
                    <div class="spec-item">
                        <div class="spec-icon">🔌</div>
                        <div>
                            <div class="spec-label">Gigabit Ethernet</div>
                            <div class="spec-value">${sw.gigabit_ports} ports</div>
                        </div>
                    </div>
                ` : ''}

                ${sw.multi_gigabit_ports > 0 ? `
                    <div class="spec-item">
                        <div class="spec-icon">⚡</div>
                        <div>
                            <div class="spec-label">Multi-Gigabit</div>
                            <div class="spec-value">${sw.multi_gigabit_ports} ports</div>
                        </div>
                    </div>
                ` : ''}

                ${sw.ten_gig_ports > 0 ? `
                    <div class="spec-item">
                        <div class="spec-icon">🚀</div>
                        <div>
                            <div class="spec-label">10 Gigabit</div>
                            <div class="spec-value">${sw.ten_gig_ports} ports</div>
                        </div>
                    </div>
                ` : ''}

                ${sw.sfp_ports > 0 ? `
                    <div class="spec-item">
                        <div class="spec-icon">📡</div>
                        <div>
                            <div class="spec-label">SFP</div>
                            <div class="spec-value">${sw.sfp_ports} ports</div>
                        </div>
                    </div>
                ` : ''}

                ${sw.sfp_plus_ports > 0 ? `
                    <div class="spec-item">
                        <div class="spec-icon">📡</div>
                        <div>
                            <div class="spec-label">SFP+</div>
                            <div class="spec-value">${sw.sfp_plus_ports} ports</div>
                        </div>
                    </div>
                ` : ''}

                ${sw.poe_support ? `
                    <div class="spec-item">
                        <div class="spec-icon">⚡</div>
                        <div>
                            <div class="spec-label">PoE</div>
                            <div class="spec-value">${poeText}</div>
                        </div>
                    </div>
                    <div class="spec-item">
                        <div class="spec-icon">🔋</div>
                        <div>
                            <div class="spec-label">Budget PoE</div>
                            <div class="spec-value">${sw.poe_budget}W</div>
                        </div>
                    </div>
                ` : ''}

                ${sw.switching_capacity ? `
                    <div class="spec-item">
                        <div class="spec-icon">💨</div>
                        <div>
                            <div class="spec-label">Capacidad</div>
                            <div class="spec-value">${sw.switching_capacity}</div>
                        </div>
                    </div>
                ` : ''}

                ${sw.managed ? `
                    <div class="spec-item">
                        <div class="spec-icon">⚙️</div>
                        <div>
                            <div class="spec-label">Gestión</div>
                            <div class="spec-value">Managed</div>
                        </div>
                    </div>
                ` : ''}

                ${sw.static_routing ? `
                    <div class="spec-item">
                        <div class="spec-icon">🛣️</div>
                        <div>
                            <div class="spec-label">Enrutamiento</div>
                            <div class="spec-value">Estático L3</div>
                        </div>
                    </div>
                ` : ''}

                ${sw.dynamic_routing ? `
                    <div class="spec-item">
                        <div class="spec-icon">🔀</div>
                        <div>
                            <div class="spec-label">Enrutamiento</div>
                            <div class="spec-value">Dinámico L3</div>
                        </div>
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

// Update the results count display
function updateResultsCount(count) {
    const countElement = document.getElementById('results-count');
    countElement.textContent = `${count} ${count === 1 ? 'switch found' : 'switches found'}`;
}

// Reset all filters to default
function resetFilters() {
    // Reset all checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });

    // Reset all number inputs
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.value = 0;
    });

    // Reapply filters (which will show all switches)
    applyFilters();
}

// Close modal with ESC key
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeModal();
    }
});

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    loadSwitchesData();
});
