"""
Componente del Formulario de Entrevista de Diagnóstico.
Fiel al documento oficial, intuitivo, ágil y con validación en vivo.
"""

import streamlit as st
from config import (
    SECTORES, RANGOS_COLABORADORES, FUENTES_ALMACENAMIENTO,
    NIVELES_INTEGRACION, FRECUENCIAS_ACTUALIZACION, NIVELES_CONFIANZA,
    TIEMPOS_REPORTE, HERRAMIENTAS_VISUALIZACION, OBSTACULOS_DECISION,
    AREAS_PRIORITARIAS, VALORES_ESPERADOS, APP_TITLE, APP_SUBTITLE, APP_DESCRIPTION
)
from scoring import evaluar_diagnostico
from database import save_interview
from components.report_view import render_report


def render_form():
    """Renderiza el formulario interactivo de recolección de entrevista."""
    
    # Si acabamos de guardar una entrevista en la sesión actual, ofrecemos verla o empezar una nueva
    if "ultima_entrevista_guardada" in st.session_state and st.session_state["ultima_entrevista_guardada"]:
        entrevista_reciente = st.session_state["ultima_entrevista_guardada"]
        st.success("✅ ¡Entrevista registrada y evaluada con éxito!")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("➕ Cargar Otra Entrevista", use_container_width=True, type="primary"):
                st.session_state["ultima_entrevista_guardada"] = None
                st.rerun()
        
        st.markdown("---")
        render_report(entrevista_reciente)
        return

    # Encabezado del Formulario
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 22px 26px; border-radius: 12px; margin-bottom: 24px;">
        <span style="background-color: #0284C7; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 600;">
            FORMULARIO OFICIAL
        </span>
        <h2 style="color: #0F172A; margin: 10px 0 4px 0; font-size: 24px; font-weight: 700;">{APP_TITLE}</h2>
        <div style="color: #64748B; font-weight: 500; font-size: 15px; margin-bottom: 8px;">{APP_SUBTITLE}</div>
        <p style="color: #475569; font-size: 14px; margin: 0; line-height: 1.5;">{APP_DESCRIPTION}</p>
        <div style="margin-top: 10px; font-size: 13px; color: #0284C7; font-weight: 600;">
            ⏱️ Tiempo estimado de respuesta: 5 a 7 minutos
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_entrevista_cliente", clear_on_submit=False):
        # Datos del Consultor
        st.caption("👤 Datos del Relevamiento")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            interviewer = st.text_input("Consultor / Entrevistador a cargo:", placeholder="Ej: Diego Martínez", value="Consultor BI")
        with col_c2:
            st.write("")
            st.caption("Este dato quedará registrado en la auditoría de la entrevista.")

        st.markdown("---")

        # -------------------------------------------------------------
        # SECCIÓN 1: DATOS GENERALES
        # -------------------------------------------------------------
        st.markdown("### 🏢 SECCIÓN 1: DATOS GENERALES")
        st.caption("Información básica de la empresa y del referente que responde.")

        col1_1, col1_2 = st.columns(2)
        with col1_1:
            interviewee_name = st.text_input("1. Nombre y Apellido del responsable *", placeholder="Ej: Juan Pérez")
            company = st.text_input("3. Nombre de la empresa u organización *", placeholder="Ej: Bodegas Andinas S.A.")

        with col1_2:
            role = st.text_input("2. Cargo / Rol en la organización", placeholder="Ej: Gerente de Operaciones / Dueño")
            employee_count = st.selectbox("5. Cantidad aproximada de colaboradores", RANGOS_COLABORADORES, index=1)

        sector = st.selectbox("4. Sector o actividad principal", SECTORES)
        sector_other = ""
        if sector == "Otro":
            sector_other = st.text_input("Especifique el sector o actividad:", placeholder="Ej: Fintech, Energía solar, etc.")

        st.markdown("---")

        # -------------------------------------------------------------
        # SECCIÓN 2: ALMACENAMIENTO Y FUENTES DE INFORMACIÓN
        # -------------------------------------------------------------
        st.markdown("### 💾 SECCIÓN 2: ALMACENAMIENTO Y FUENTES DE INFORMACIÓN")
        st.caption("Identificación de repositorios, sistemas transaccionales e integración actual.")

        st.markdown("**6. ¿Dónde se registra y almacena hoy la mayor parte de la información operativa y comercial?** *(Seleccione todas las que apliquen)*")
        storage_sources = []
        col2_a, col2_b = st.columns(2)
        for idx, fuente in enumerate(FUENTES_ALMACENAMIENTO):
            col_target = col2_a if idx % 2 == 0 else col2_b
            with col_target:
                if fuente == "Otro":
                    chk_otro = st.checkbox("Otro medio o repositorio", key="chk_fuente_otro")
                    if chk_otro:
                        storage_sources.append("Otro")
                else:
                    if st.checkbox(fuente, key=f"fuente_{idx}"):
                        storage_sources.append(fuente)

        storage_other = ""
        if "Otro" in storage_sources:
            storage_other = st.text_input("Especifique otro medio de almacenamiento:", placeholder="Ej: Access, Notion, etc.")

        st.markdown("<br>", unsafe_allow_html=True)
        integration_level = st.radio(
            "7. ¿Cómo calificaría la integración entre sus distintas áreas (ventas, compras, administración, operaciones)?",
            NIVELES_INTEGRACION,
            index=1
        )

        st.markdown("---")

        # -------------------------------------------------------------
        # SECCIÓN 3: RECOLECCIÓN, ACTUALIZACIÓN Y CALIDAD
        # -------------------------------------------------------------
        st.markdown("### 🔄 SECCIÓN 3: RECOLECCIÓN, ACTUALIZACIÓN Y CALIDAD")
        st.caption("Dinámica de refresco y confiabilidad percibida de la información.")

        col3_1, col3_2 = st.columns(2)
        with col3_1:
            update_frequency = st.radio(
                "8. ¿Con qué frecuencia se actualizan los datos clave del negocio?",
                FRECUENCIAS_ACTUALIZACION,
                index=1
            )

        with col3_2:
            data_confidence = st.radio(
                "9. ¿Qué nivel de confianza tiene en la consistencia de sus datos actuales?",
                NIVELES_CONFIANZA,
                index=1
            )

        st.markdown("---")

        # -------------------------------------------------------------
        # SECCIÓN 4: GENERACIÓN DE REPORTES Y TOMA DE DECISIONES
        # -------------------------------------------------------------
        st.markdown("### 📊 SECCIÓN 4: GENERACIÓN DE REPORTES Y TOMA DE DECISIONES")
        st.caption("Tiempos de preparación, herramientas y principales fricciones directivas.")

        col4_1, col4_2 = st.columns(2)
        with col4_1:
            report_time = st.radio(
                "10. ¿Cuánto tiempo le toma a su equipo consolidar los reportes periódicos de gestión?",
                TIEMPOS_REPORTE,
                index=0
            )

        with col4_2:
            current_bi_tool = st.radio(
                "11. ¿Qué herramienta utilizan actualmente para visualizar y analizar los indicadores?",
                HERRAMIENTAS_VISUALIZACION,
                index=0
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**12. ¿Cuáles son los principales obstáculos que enfrenta la dirección al momento de tomar decisiones?** *(Marque hasta 3)*")
        decision_obstacles = []
        for idx, obs in enumerate(OBSTACULOS_DECISION):
            if st.checkbox(obs, key=f"obs_{idx}"):
                decision_obstacles.append(obs)

        if len(decision_obstacles) > 3:
            st.warning("⚠️ Ha marcado más de 3 obstáculos. Le sugerimos priorizar los 3 más críticos para un diagnóstico más certero.")

        st.markdown("---")

        # -------------------------------------------------------------
        # SECCIÓN 5: PRIORIDADES Y EXPECTATIVAS
        # -------------------------------------------------------------
        st.markdown("### 🎯 SECCIÓN 5: PRIORIDADES Y EXPECTATIVAS")
        st.caption("Foco de negocio deseado y retorno esperado de la iniciativa de BI.")

        col5_1, col5_2 = st.columns(2)
        with col5_1:
            priority_process = st.selectbox(
                "13. ¿Cuál sería el área o proceso prioritario para implementar su primer tablero interactivo?",
                AREAS_PRIORITARIAS
            )
            priority_other = ""
            if priority_process == "Otro":
                priority_other = st.text_input("Especifique el área o proceso prioritario:", placeholder="Ej: Control de mermas, logística de última milla, etc.")

        with col5_2:
            expected_value = st.radio(
                "14. ¿Qué valor principal espera obtener de la implementación de Business Intelligence en su empresa?",
                VALORES_ESPERADOS,
                index=0
            )

        st.markdown("---")

        # NOTAS ADICIONALES DEL CONSULTOR
        st.markdown("### 📝 Notas y Observaciones del Consultor")
        consultant_notes = st.text_area(
            "Comentarios cualitativos, tono del cliente, sistemas específicos mencionados o próximos pasos:",
            placeholder="Ej: El cliente planea cambiar de ERP el año próximo. Tienen urgencia en el módulo de ventas y cobranzas. Muy receptivo a Power BI.",
            height=90
        )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Finalizar Entrevista y Calcular Diagnóstico", type="primary", use_container_width=True)

    if submitted:
        # Validaciones básicas
        if not company.strip():
            st.error("❌ Por favor ingrese el Nombre de la empresa u organización.")
            return
        if not interviewee_name.strip():
            st.error("❌ Por favor ingrese el Nombre y Apellido del responsable.")
            return

        # Armar payload
        datos_entrevista = {
            "interviewer": interviewer.strip(),
            "interviewee_name": interviewee_name.strip(),
            "role": role.strip(),
            "company": company.strip(),
            "sector": sector,
            "sector_other": sector_other.strip(),
            "employee_count": employee_count,
            "storage_sources": storage_sources,
            "storage_other": storage_other.strip(),
            "integration_level": integration_level,
            "update_frequency": update_frequency,
            "data_confidence": data_confidence,
            "report_time": report_time,
            "current_bi_tool": current_bi_tool,
            "decision_obstacles": decision_obstacles,
            "priority_process": priority_process,
            "priority_other": priority_other.strip(),
            "expected_value": expected_value,
            "consultant_notes": consultant_notes.strip(),
            "status": "Completada"
        }

        # Calcular diagnóstico oficial
        diag = evaluar_diagnostico(datos_entrevista)
        datos_entrevista["maturity_score"] = diag["score_global"]
        datos_entrevista["maturity_level"] = diag["nivel"]
        datos_entrevista["dimension_scores"] = diag["dimensiones"]

        # Guardar en SQLite
        nuevo_id = save_interview(datos_entrevista)
        
        # Recuperar entrevista completa guardada
        from database import get_interview
        guardado = get_interview(nuevo_id)
        st.session_state["ultima_entrevista_guardada"] = guardado
        st.session_state["mensaje_exito"] = f"Entrevista de {company} guardada con éxito (ID #{nuevo_id})."
        st.rerun()
