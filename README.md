# EnGenius Switch Filter

Aplicación web para filtrar y comparar switches EnGenius según especificaciones técnicas.

## Características

### Filtros Disponibles

#### Tipo de Puertos
- **Gigabit Ethernet**: Filtra por cantidad mínima de puertos 10/100/1000 Mbps
- **Multi-Gigabit**: Filtra por puertos 2.5G/5G
- **10 Gigabit Ethernet**: Filtra por puertos 10G
- **SFP**: Filtra por puertos SFP
- **SFP+**: Filtra por puertos SFP+ (10G)

#### Power over Ethernet (PoE)
- **Soporte PoE**: Switches con capacidad PoE
- **PoE (802.3af)**: Hasta 15.4W por puerto
- **PoE+ (802.3at)**: Hasta 30W por puerto
- **PoE++ (802.3bt)**: Hasta 60W/90W por puerto
- **Presupuesto PoE Mínimo**: Watts totales disponibles para PoE

#### Gestión y Características
- **Switch Gestionado**: Switches con capacidades de gestión avanzada
- **DHCP Snooping**: Seguridad contra ataques DHCP
- **IGMP Snooping**: Gestión eficiente de tráfico multicast

#### Capa de Red
- **Capa 2 (L2/L2+)**: Switches de capa 2 con características avanzadas
- **Enrutamiento Estático L3**: Capacidad de enrutamiento estático
- **Enrutamiento Dinámico L3**: Protocolos de enrutamiento dinámico (RIP, OSPF, BGP)

## Archivos del Proyecto

- **index.html**: Interfaz de usuario de la aplicación
- **app.js**: Lógica de filtrado y visualización
- **switches_data.json**: Base de datos de switches procesada
- **process_switch_data.py**: Script para procesar datos del Excel a JSON
- **convert_to_csv.py**: Script para convertir Excel a CSV
- **server.py**: Servidor HTTP local para desarrollo

## Uso

### 1. Convertir Excel a CSV (ya completado)
```bash
python3 convert_to_csv.py
```

### 2. Procesar datos a JSON (ya completado)
```bash
python3 process_switch_data.py
```

### 3. Iniciar el servidor web
```bash
python3 server.py
```

### 4. Abrir en el navegador
Abre http://localhost:8000 en tu navegador favorito

## Datos Procesados

La aplicación incluye información de **23 switches EnGenius**:
- 17 switches de la serie CloudSwitch (ECS)
- 6 switches de la serie FitSwitch (EWS-FIT)

### Características Detectadas
- Switches con PoE: 17
- Switches con Multi-Gigabit: 7
- Switches con SFP+: 15
- Todos incluyen enrutamiento estático L3

## Tecnologías Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python 3
- **Procesamiento de Datos**: openpyxl, csv, json
- **Servidor**: http.server (Python)

## Estructura de Datos

Cada switch contiene:
```json
{
  "model_name": "Nombre del modelo",
  "model_number": "Número de modelo",
  "gigabit_ports": 0,
  "multi_gigabit_ports": 0,
  "sfp_ports": 0,
  "sfp_plus_ports": 0,
  "ten_gig_ports": 0,
  "poe_support": false,
  "poe_af": false,
  "poe_at": false,
  "poe_bt": false,
  "poe_budget": 0,
  "managed": true,
  "layer": "L2/L2+/L3",
  "dhcp_relay": false,
  "dhcp_snooping": false,
  "igmp_snooping": false,
  "static_routing": false,
  "dynamic_routing": false,
  "switching_capacity": ""
}
```

## Mejoras Futuras Sugeridas

1. Exportar resultados filtrados a CSV/PDF
2. Comparación lado a lado de hasta 3 switches
3. Ordenamiento por diferentes criterios (precio, capacidad, puertos)
4. Búsqueda por texto (modelo, número)
5. Filtros adicionales:
   - Consumo energético máximo
   - Dimensiones físicas
   - Factor de forma (desktop, rack 1U)
   - Capacidad de switching
   - Cantidad de VLANs soportadas
   - QoS (Quality of Service)
   - Seguridad (ACL, Port Security, 802.1X)

## Licencia

Proyecto desarrollado para EnGenius
