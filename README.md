# 📊 I+S Data Solutions — Diagnóstico de Madurez de Datos & Business Intelligence (BI)

Aplicación desarrollada en **Python** y **Streamlit**, diseñada para relevar de forma ágil y profesional entrevistas de diagnóstico con clientes sobre el estado de sus datos, dimensionar sus necesidades analíticas y presentar propuestas comerciales personalizadas.

Está basada estrictamente en el **Formulario de Diagnóstico: Estado y Madurez de Datos (Evaluación Inicial para Business Intelligence)** y su **Matriz Interna de Evaluación**, complementado con la **Propuesta de Trabajo Institucional de I+S Data Solutions**.

---

## 🚀 Módulos y Características Principales

### 1. 📝 Formulario de Diagnóstico Oficial (5 a 7 minutos)
- **Sección 1:** Datos Generales (Responsable, Cargo, Empresa, Sector, Colaboradores).
- **Sección 2:** Almacenamiento y Fuentes de Información (Planillas, ERP, CRM, Facturación, Papel, Integración 1 a 4).
- **Sección 3:** Recolección, Actualización y Calidad (Frecuencia de datos y Nivel de confianza).
- **Sección 4:** Generación de Reportes y Toma de Decisiones (Tiempos de reporte, herramientas actuales y principales obstáculos).
- **Sección 5:** Prioridades y Expectativas (Proceso prioritario a modelar y valor esperado del BI).
- **Notas del Consultor:** Campo dedicado para registrar percepciones y detalles cualitativos durante la reunión.

### 2. 🎯 Diagnóstico Automático en Tiempo Real
- Cálculo automático de **Puntaje Global (0 a 100)** y desglose por 5 dimensiones:
  - *Almacenamiento y Fuentes*
  - *Integración entre Áreas*
  - *Frecuencia de Actualización*
  - *Calidad y Consistencia*
  - *Eficiencia de Reportes*
- Clasificación oficial según la **Matriz Interna de Evaluación**:
  - 🔴 **Nivel 1: Inicial / Disperso** *(Normalización y Tablero Base)*
  - 🟡 **Nivel 2: Operativo / Estructurado** *(Pipeline y Data Modeling)*
  - 🟢 **Nivel 3: Avanzado / Preparado** *(BI Integral & Analítica Predictiva)*
- Visualización con **Gráfico de Gauge** y **Radar Dimensional** (Plotly).
- Generación del **Plan de Acción de 4 Pasos** y descarga del informe resumido en `.txt`.

### 3. 💼 Propuesta de Servicios y Modelo de Trabajo (I+S Data Solutions)
- **Propuesta Institucional**:
  - *Quiénes Somos:* Filosofía de transformación de registros dispersos en sistemas de control visual.
  - *Pipeline de 4 Fases:* Fuentes de Datos → Integración y Consistencia → Tableros Interactivos → Decisión Asertiva.
  - *Problemas Resueltos:* Fin de planillas incompatibles, eliminación de horas manuales y detección de desvíos.
  - *Trayectoria y Respaldo:* Agroindustria/olivícola, instituciones profesionales y cámaras sectoriales.
  - *Contacto:* E. Carriego N° 431, La Rioja, Argentina.
- **Generador de Propuesta Personalizada por Cliente**:
  - Selecciona cualquier entrevista de la base de datos.
  - Adapta automáticamente el objetivo, alcance y plan técnico al proceso prioritario del cliente.
  - Botón de descarga de la propuesta comercial formal en `.txt`.

### 4. 📋 Panel de Administración Completo
- Búsqueda en tiempo real por empresa, entrevistado o consultor.
- Filtros por Nivel de Madurez y Sector Económico.
- Botón directo para inspeccionar el informe completo de cualquier cliente.
- Edición rápida de notas u observaciones y estado de la entrevista.
- Eliminación segura con confirmación.
- **Exportación inmediata**:
  - 📊 **Excel (.xlsx)** estructurado.
  - 📄 **CSV (.csv)** para análisis rápido.
  - 📦 **JSON (.json)** para integración con otras bases.

### 5. 📊 Analítica Global del Portafolio
- Métricas globales consolidadas.
- Distribución de clientes por nivel de madurez.
- Gráfico de sectores económicos relevados.
- Análisis de frecuencia de obstáculos directivos (cuellos de botella del mercado).
- Procesos de negocio más demandados para implementar BI.
- Radar comparativo del promedio general de las empresas.

### 6. 💾 Persistencia Local y Cero Configuración
- Base de datos **SQLite local (`entrevistas_bi.db`)**, autogestionada sin necesidad de servidores adicionales.
- Incluye botón de **"Sembrar Datos de Prueba"** para demostraciones inmediatas.

---

## 💻 Cómo Ejecutar Localmente

1. **Abrir la terminal o PowerShell** en la carpeta del proyecto:
   ```powershell
   cd "C:\Users\diego\.gemini\antigravity-ide\scratch\bi_diagnostico_app"
   ```

2. **Ejecutar con Streamlit:**
   ```powershell
   streamlit run app.py
   ```

3. La aplicación se abrirá en su navegador en `http://localhost:8501`.

---

## ☁️ Publicación en Streamlit Community Cloud

Para desplegar la aplicación gratis y compartirla con clientes:

1. Ve a [share.streamlit.io](https://share.streamlit.io).
2. Conecta tu repositorio: `diego305/i-s-Data-Solution`.
3. Especifica la rama `main` y el archivo `app.py`.
4. Haz clic en **Deploy**.

---

## 📂 Estructura del Repositorio

```
i-s-Data-Solution/
│
├── app.py                      # Punto de entrada principal y menú lateral
├── config.py                   # Preguntas, opciones y Matriz Oficial de Evaluación
├── scoring.py                  # Algoritmo de cálculo de madurez y diagnóstico
├── database.py                 # Persistencia en SQLite (CRUD + Seeder)
├── requirements.txt            # Dependencias del proyecto
├── .gitignore                  # Exclusiones de Git
├── README.md                   # Documentación detallada
│
└── components/
    ├── form_view.py            # Formulario interactivo con las 5 secciones
    ├── proposal_view.py        # Propuesta institucional y a medida por cliente
    ├── admin_view.py           # Panel administrativo y exportaciones
    ├── report_view.py          # Informe ejecutivo con gauge, radar y recomendaciones
    └── analytics_view.py       # Dashboard analítico de clientes relevados
```
