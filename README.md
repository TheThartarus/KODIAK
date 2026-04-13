# KODIAK 🐻
**Sistema de Gestión Administrativa y Servicio Comunitario**

KODIAK es una herramienta integral desarrollada en Python para automatizar el registro, control y seguimiento de ciudadanos en procesos administrativos judiciales (específicamente en el Circuito Judicial de los Valles del Tuy).

## 🚀 Funcionalidades

* **Gestión de Expedientes (CRUD):** Registro, búsqueda, actualización y eliminación de ciudadanos de forma intuitiva.
* **Automatización de Documentos:**
    * Creación automática de carpetas organizadas por **CDI y Nombre**.
    * Extracción y preparación de hojas de asistencia desde plantillas comprimidas.
    * **Certificación:** Generación instantánea de certificaciones finales (Word) directamente en la carpeta del ciudadano.
* **Reportes y Exportación:**
    * Exportación de la base de datos a **Excel (.xlsx)** mediante `openpyxl`.
* **Seguridad y Respaldo:**
    * **Backup:** Copia de seguridad automática del registro CSV en `Mis Documentos/KODIAK/Backup` cada vez que se guarda un nuevo dato.
* **Estadísticas:** Visualización en tiempo real de métricas clave (por el momento, sólo el total de ciudadanos registrados).

## 🛠️ Requisitos

* **Lenguaje:** Python 3.x
* **Interfaz Gráfica:** Tkinter (Nativa)
* **Dependencias Externas:**
    ```bash
    pip install openpyxl
    ```
* **Sistema Operativo:** Optimizado para **Windows** (Manejo de rutas nativas y acceso al Explorador de Archivos).

## 📂 Estructura del Proyecto

```text
KODIAK/
│
├── main.py                 # Ventana principal y controlador de la App
├── core/                   # Lógica modular del sistema
│   ├── save_record.py      # Guardado, validación y Backup
│   ├── find_record.py      # Búsqueda y apertura de carpetas
│   ├── update_record.py    # Edición de registros y renombrado de directorios
│   ├── remove_record.py    # Eliminación segura de datos y archivos
│   ├── export_data.py      # Motor de generación de Excel profesional
│   ├── generate_docs.py    # Extracción de modelos Word desde ZIP
│   ├── stats.py            # Dashboard de estadísticas descriptivas
│   └── about.py            # Información de autoría (Créditos)
│
├── data/                   # Almacén de carpetas de ciudadanos (Generado)
├── records.csv             # Base de datos principal en formato plano
└── MODELS.zip              # Contenedor de plantillas (ASISTENCIA, MODELOS)
```
## ©️ Créditos

**Desarrollado por:** The Thartarus