#!/usr/bin/env python3
"""
Script to translate the application from Spanish to English
"""

# Translations dictionary
translations = {
    # HTML translations
    'Comparador de Switches': 'Switch Comparator',
    'Encuentra el switch perfecto para tus necesidades': 'Find the perfect switch for your needs',
    'Tipo de Puertos': 'Port Types',
    'Gigabit Ethernet': 'Gigabit Ethernet',
    'Multi-Gigabit': 'Multi-Gigabit',
    'Mínimo': 'Minimum',
    'Puertos Avanzados': 'Advanced Ports',
    'Power over Ethernet': 'Power over Ethernet',
    'Soporte PoE': 'PoE Support',
    'Presupuesto': 'Budget',
    'Características': 'Features',
    'Capa de Red': 'Network Layer',
    'Enrutamiento Estático': 'Static Routing',
    'Enrutamiento Dinámico': 'Dynamic Routing',
    'Restablecer Filtros': 'Reset Filters',
    'Cargando switches': 'Loading switches',

    # JS translations
    'puertos': 'ports',
    'puertos totales': 'total ports',
    'puerto': 'port',
    'Gestionado': 'Managed',
    'Configuración de Puertos': 'Port Configuration',
    'Puertos Gigabit Ethernet': 'Gigabit Ethernet Ports',
    'Puertos Multi-Gigabit (2.5G/5G)': 'Multi-Gigabit Ports (2.5G/5G)',
    'Puertos 10 Gigabit': '10 Gigabit Ports',
    'Puertos SFP': 'SFP Ports',
    'Puertos SFP+': 'SFP+ Ports',
    'Estándares PoE': 'PoE Standards',
    'Presupuesto Total PoE': 'Total PoE Budget',
    'Rendimiento': 'Performance',
    'Capacidad de Switching': 'Switching Capacity',
    'Capa de Red': 'Network Layer',
    'Características de Red': 'Network Features',
    'Switch Gestionado': 'Managed Switch',
    'Enrutamiento Estático L3': 'L3 Static Routing',
    'Enrutamiento Dinámico (RIP/OSPF)': 'Dynamic Routing (RIP/OSPF)',
    'Hardware': 'Hardware',
    'Interfaces de Gestión': 'Management Interfaces',
    'Características L2 Avanzadas': 'Advanced L2 Features',
    'Seguridad': 'Security',
    'Especificaciones Físicas': 'Physical Specifications',
    'Fuente de Alimentación': 'Power Source',
    'Temperatura de Operación': 'Operating Temperature',
    'Humedad de Operación': 'Operating Humidity',
    'Dimensiones': 'Dimensions',
    'Peso': 'Weight',
    'Resumen Total de Puertos': 'Total Ports Summary',
    'No se encontraron switches': 'No switches found',
    'Intenta ajustar los filtros para ver más resultados': 'Try adjusting the filters to see more results',
    'switch encontrado': 'switch found',
    'switches encontrados': 'switches found',
    'Access Control Lists (ACL)': 'Access Control Lists (ACL)',
    'QoS': 'QoS',
    'Queues': 'Queues',
}

print("Translating application to English...\n")

# Read the app.js file
with open('app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Apply translations to JS
for spanish, english in translations.items():
    js_content = js_content.replace(spanish, english)

# Write back
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("✓ app.js translated to English")

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Apply translations to HTML
for spanish, english in translations.items():
    html_content = html_content.replace(spanish, english)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ index.html translated to English")
print("\n✓ Translation completed successfully!")
print("✓ Reload http://localhost:8080 to see changes")
