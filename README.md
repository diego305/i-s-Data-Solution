# 📊 Aplicación de Diagnóstico de Madurez de Datos & Business Intelligence (BI)

Aplicación desarrollada en **Python** y **Streamlit**, diseñada para relevar de forma ágil y profesional entrevistas de diagnóstico con clientes sobre el estado de sus datos y sus necesidades de Business Intelligence.

Está basada estrictamente en el **Formulario de Diagnóstico: Estado y Madurez de Datos (Evaluación Inicial para Business Intelligence)** y su **Matriz Interna de Evaluación**.

---

## 🚀 Características Principales

1. **Formulario Ágil de Entrevista (5 a 7 minutos):**
   - **Sección 1:** Datos Generales (Responsable, Cargo, Empresa, Sector, Colaboradores).
   - **Sección 2:** Almacenamiento y Fuentes de Información (Planillas, ERP, CRM, Facturación, Papel, Integración 1 a 4).
   - **Sección 3:** Recolección, Actualización y Calidad (Frecuencia de datos y Nivel de confianza).
   - **Sección 4:** Generación de Reportes y Toma de Decisiones (Tiempos de reporte, herramientas actuales y principales obstáculos).
   - **Sección 5:** Prioridades y Expectativas (Proceso prioritario a modelar y valor esperado del BI).
   - **Notas del Consultor:** Campo dedicado para registrar percepciones y detalles cualitativos durante la reunión.

2. **Diagnóstico Automático en Tiempo Real:**
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
   - Generación del **Plan de Acción de 4 Pasos** y descarga del informe en `.txt`.

3. **Panel de Administración Completo ("Fácil de Administrar"):**
   - Búsqueda en tiempo real por empresa, entrevistado o consultor.
   - Filtros por Nivel de Madurez y Sector Económico.
   - Botón directo para inspeccionar el informe completo de cualquier cliente.
   - Edición rápida de notas u observaciones y estado de la entrevista.
   - Eliminación segura con confirmación.
   - **Exportación inmediata** a:
     - 📊 **Excel (.xlsx)** con formato tabular completo.
     - 📄 **CSV (.csv)** para cruces analíticos rápidos.
     - 📦 **JSON (.json)** para integración con otras bases.

4. **Analítica Global del Portafolio:**
   - Métricas globales consolidadas.
   - Distribución de clientes por nivel de madurez.
   - Gráfico de sectores económicos relevados.
   - Análisis de frecuencia de obstáculos directivos (cuellos de botella del mercado).
   - Procesos de negocio más demandados para implementar BI.
   - Radar comparativo del promedio general de las empresas.

5. **Persistencia Local y Cero Configuración:**
   - Base de datos **SQLite local (`entrevistas_bi.db`)**, autogestionada sin necesidad de servidores adicionales.
   - Incluye botón de **"Sembrar Datos de Prueba"** para demostraciones inmediatas.

---

## 💻 Cómo Ejecutar la Aplicación

1. **Abrir la terminal o PowerShell** en la carpeta del proyecto:
   ```powershell
   cd "C:\Users\diego\.gemini\antigravity-ide\scratch\bi_diagnostico_app"
   ```

2. **Ejecutar con Streamlit:**
   ```powershell
   streamlit run app.py
   ```

3. La aplicación se abrirá automáticamente en su navegador en `http://localhost:8501`.

---

## 📂 Estructura del Proyecto

```
bi_diagnostico_app/
│
├── app.py                      # Punto de entrada principal y enrutador
├── config.py                   # Preguntas, opciones y Matriz Oficial de Evaluación
├── scoring.py                  # Algoritmo de cálculo de madurez y diagnóstico
├── database.py                 # Persistencia en SQLite (CRUD + Seeder)
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación detallada
│
└── components/
    ├── form_view.py            # Formulario interactivo con las 5 secciones
    ├── admin_view.py           # Panel administrativo y exportaciones
    ├── report_view.py          # Informe ejecutivo con gauge, radar y recomendaciones
    └── analytics_view.py       # Dashboard analítico de clientes relevados
```
