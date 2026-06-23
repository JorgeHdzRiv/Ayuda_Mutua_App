# Sistema de Gestión - Fundación Ayuda Mutua

Plataforma web desarrollada como proyecto de ingeniería de software para optimizar la gestión operativa de la Fundación Ayuda Mutua. El sistema automatiza el registro de donativos, la organización de eventos y el control de inventario, proporcionando dashboards administrativos para la toma de decisiones basada en datos.

## 🚀 Características principales
* **Gestión de Donativos:** Registro detallado con asignación automática de folios y trazabilidad.
* **Dashboard Administrativo:** Visualización en tiempo real de indicadores clave (donativos, donantes activos, eventos).
* **Control de Inventario:** Monitoreo de artículos disponibles para las actividades de la fundación.
* **Arquitectura Escalable:** Desarrollado bajo un modelo de 3 capas para asegurar la integridad y el rendimiento de los datos.

## 🛠 Stack Tecnológico
* **Lenguaje:** Python
* **Framework Web:** [Streamlit](https://streamlit.io/)
* **Base de Datos:** PostgreSQL (via Supabase)
* **Visualización:** Pandas, Plotly
* **Despliegue:** Streamlit Community Cloud

## 🏗 Arquitectura del Sistema
El sistema se basa en una arquitectura de 3 capas:
1. **Capa de Presentación:** Interfaz intuitiva desarrollada en Streamlit.
2. **Capa de Lógica de Negocio:** Validación de datos, cálculos financieros y reglas de negocio en Python.
3. **Capa de Datos:** Persistencia en base de datos relacional para consulta y almacenamiento seguro.

## 📋 Estructura del Proyecto
```text
├── app.py              # Punto de entrada de la aplicación
├── database.py         # Módulo de conexión a base de datos
├── requirements.txt    # Dependencias del proyecto
├── assets/             # Imágenes y bocetos de interfaz
└── README.md
```

## 🚀 Instalación Local
* Clona el repositorio:
```
git clone https://github.com/JorgeHdzRiv/Ayuda_Mutua_App
```

* Instala las dependencias:
```
pip install -r requirements.txt
```

* Ejecuta la aplicación:
```
streamlit run app.py
```