"""
Componente para visualizar la Propuesta de Trabajo de I+S DATA SOLUTIONS.
Incluye presentación institucional de servicios y generador de propuesta personalizada según el diagnóstico del cliente.
"""

import streamlit as st
from database import get_all_interviews, get_interview
from config import MATRIZ_EVALUACION


def render_proposal():
    """Renderiza la sección de Propuesta de Trabajo institucional y personalizada."""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 28px 32px; border-radius: 14px; color: white; margin-bottom: 24px; border: 1px solid #334155;">
        <span style="background: rgba(2, 132, 199, 0.3); color: #38BDF8; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 700; border: 1px solid rgba(56, 189, 248, 0.4);">
            I+S DATA SOLUTIONS
        </span>
        <h1 style="margin: 12px 0 6px 0; font-size: 28px; font-weight: 800; color: #F8FAFC;">
            Propuesta de Servicios y Modelo de Trabajo
        </h1>
        <p style="margin: 0; color: #94A3B8; font-size: 16px; font-weight: 500;">
            Inteligencia de Datos para Decisiones Estratégicas
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_institucional, tab_personalizada = st.tabs([
        "🏢 Propuesta Institucional (Servicios)",
        "🎯 Propuesta Personalizada por Cliente"
    ])

    with tab_institucional:
        # 1. QUIÉNES SOMOS
        st.markdown("### 1. Quiénes Somos y Filosofía")
        st.markdown("""
        > *"El valor real no está en acumular datos, sino en saber utilizarlos para decidir mejor."*
        
        En un entorno productivo y comercial cada vez más dinámico, las organizaciones no sufren por falta de información, sino por la dificultad de procesarla a tiempo y con precisión.
        
        **I+S Data Solutions** es una consultora interdisciplinaria que ayuda a empresas, instituciones y unidades productivas a transformar registros dispersos en **sistemas visuales de control y análisis en tiempo real**. Conectamos la realidad operativa con herramientas modernas de Business Intelligence para que cada decisión estratégica esté respaldada por evidencia concreta y confiable.
        """)

        st.markdown("---")

        # 2. NUESTRO ENFOQUE
        st.markdown("### 2. Nuestro Enfoque: De los datos aislados a la acción concreta")
        
        # Pipeline visual interactivo
        col_f1, col_f2, col_f3, col_f4 = st.columns(4)
        with col_f1:
            st.markdown("""
            <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-top: 4px solid #64748B; border-radius: 10px; padding: 16px; text-align: center; height: 100%;">
                <div style="font-size: 24px; margin-bottom: 6px;">📂</div>
                <strong style="color: #0F172A; font-size: 14px;">1. Fuentes de Datos</strong>
                <p style="font-size: 12.5px; color: #64748B; margin-top: 6px;">Planillas, ERP, sistemas de facturación y CRM dispersos.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_f2:
            st.markdown("""
            <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-top: 4px solid #0284C7; border-radius: 10px; padding: 16px; text-align: center; height: 100%;">
                <div style="font-size: 24px; margin-bottom: 6px;">⚙️</div>
                <strong style="color: #0284C7; font-size: 14px;">2. Integración y Consistencia</strong>
                <p style="font-size: 12.5px; color: #64748B; margin-top: 6px;">Limpieza, normalización y diccionario de métricas único.</p>
            </div>
            """, unsafe_allow_html=True)

        with col_f3:
            st.markdown("""
            <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-top: 4px solid #8B5CF6; border-radius: 10px; padding: 16px; text-align: center; height: 100%;">
                <div style="font-size: 24px; margin-bottom: 6px;">📊</div>
                <strong style="color: #8B5CF6; font-size: 14px;">3. Tableros Interactivos</strong>
                <p style="font-size: 12.5px; color: #64748B; margin-top: 6px;">Dashboards en la nube para PC y celular con filtros ágiles.</p>
            </div>
            """, unsafe_allow_html=True)

        with col_f4:
            st.markdown("""
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-top: 4px solid #10B981; border-radius: 10px; padding: 16px; text-align: center; height: 100%;">
                <div style="font-size: 24px; margin-bottom: 6px;">🎯</div>
                <strong style="color: #065F46; font-size: 14px;">4. Decisión Asertiva</strong>
                <p style="font-size: 12.5px; color: #047857; margin-top: 6px;">Anticipación de desvíos, ahorro de horas y rentabilidad.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.markdown("**🔹 Objetividad:** Métricas estandarizadas sin interpretaciones contradictorias entre departamentos.")
        with col_p2:
            st.markdown("**🔹 Oportunidad:** Disponibilidad de indicadores clave en tiempo real, sin demoras operativas.")
        with col_p3:
            st.markdown("**🔹 Claridad:** Información visual, interactiva y accesible para los niveles directivos y mandos medios.")

        st.markdown("---")

        # 3. NUESTRO PRODUCTO
        st.markdown("### 3. Nuestro Producto: Business Intelligence y Analítica de Gestión")
        st.markdown("""
        Un servicio integral diseñado para ordenar el ecosistema de información de su empresa y desplegar tableros de control interactivos que simplifican el seguimiento de sus objetivos.
        """)

        col_q1, col_q2 = st.columns([1, 1.4])
        with col_q1:
            st.markdown("""
            <div style="background: #FFFBEB; border-left: 4px solid #F59E0B; padding: 16px; border-radius: 8px;">
                <h4 style="margin: 0 0 8px 0; color: #B45309; font-size: 15px;">¿Qué problemas resolvemos?</h4>
                <ul style="margin: 0; padding-left: 18px; color: #78350F; font-size: 13.5px; line-height: 1.5;">
                    <li style="margin-bottom: 6px;"><strong>Fin de planillas fragmentadas:</strong> Eliminamos inconsistencias entre archivos que no coinciden.</li>
                    <li style="margin-bottom: 6px;"><strong>Ahorro de horas manuales:</strong> Chau al armado repetitivo y estresante de reportes a fin de mes.</li>
                    <li><strong>Detección temprana de desvíos:</strong> Alertas visibles en costos, márgenes, compras y cobranzas.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col_q2:
            st.markdown("""
            <div style="background: white; border: 1px solid #E2E8F0; padding: 16px; border-radius: 8px;">
                <h4 style="margin: 0 0 10px 0; color: #0F172A; font-size: 15px;">Fases y Componentes de la Solución:</h4>
                <div style="margin-bottom: 8px;">
                    <strong style="color: #0284C7; font-size: 13.5px;">1. Auditoría e Integración de Fuentes:</strong>
                    <div style="color: #475569; font-size: 13px;">Conectamos y normalizamos sus datos existentes (ERP, hojas de cálculo, comprobantes fiscales, CRM).</div>
                </div>
                <div style="margin-bottom: 8px;">
                    <strong style="color: #0284C7; font-size: 13.5px;">2. Modelado y Gobernanza de Indicadores:</strong>
                    <div style="color: #475569; font-size: 13px;">Definición precisa de sus KPIs críticos con un diccionario unificado de métricas.</div>
                </div>
                <div style="margin-bottom: 8px;">
                    <strong style="color: #0284C7; font-size: 13.5px;">3. Despliegue de Tableros Interactivos (Dashboards):</strong>
                    <div style="color: #475569; font-size: 13px;">Implementación en la nube para explorar datos con filtros por período, zona, producto o responsable.</div>
                </div>
                <div>
                    <strong style="color: #0284C7; font-size: 13.5px;">4. Capacitación y Adopción:</strong>
                    <div style="color: #475569; font-size: 13px;">Transferencia práctica al equipo directivo y operativo para garantizar uso autónomo continuo.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # 4. TRAYECTORIA Y RESPALDO
        st.markdown("### 4. Trayectoria y Respaldo")
        st.markdown("""
        Contamos con una sólida experiencia en el análisis y sistematización de datos estratégicos para sectores clave de la región:
        
        * 🍇 **Sector Agroindustrial y Olivícola:** Elaboración de sinopsis estadísticas, mapeos territoriales, costos y rendimientos productivos.
        * 🏛️ **Instituciones y Cámaras Sectoriales:** Desarrollo de plataformas y herramientas de gestión de información para organismos de desarrollo productivo y colegios profesionales.
        * 📈 **Consultoría Empresarial:** Asesoramiento técnico en estructuración de flujos de datos para la toma de decisiones gerenciales.
        """)

        st.markdown("---")

        # 5. CONTACTO
        st.markdown("### 5. Contacto e Inicio de Proyecto")
        st.markdown("""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px;">
            <strong style="color: #0F172A; font-size: 15px;">Comience a gestionar su organización sobre bases sólidas:</strong>
            <div style="margin-top: 10px; color: #475569; font-size: 14px; line-height: 1.6;">
                📍 <strong>Ubicación:</strong> E. Carriego N° 431, La Rioja, Argentina.<br>
                ✨ <strong>Diagnóstico inicial sin cargo:</strong> Evaluamos el estado actual de los datos de su empresa y le presentamos una propuesta a medida para su primer tablero de control.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab_personalizada:
        st.markdown("### Generador de Propuesta Comercial a Medida")
        st.caption("Adapta automáticamente la propuesta institucional con los resultados del diagnóstico del cliente.")

        df_clientes = get_all_interviews()
        if df_clientes.empty:
            st.info("ℹ️ No hay clientes relevados en la base de datos para generar una propuesta personalizada.")
        else:
            opciones_clientes = {
                f"{row['empresa']} (Resp: {row['responsable_nombre']} - {row['nivel_madurez'].split(':')[0]})": int(row['id'])
                for _, row in df_clientes.iterrows()
            }
            cliente_sel_label = st.selectbox("Seleccione el cliente entrevistado:", list(opciones_clientes.keys()))
            cid = opciones_clientes[cliente_sel_label]
            cliente = get_interview(cid)

            if cliente:
                empresa = cliente.get("empresa", "")
                responsable = cliente.get("responsable_nombre", "")
                rol = cliente.get("responsable_rol", "")
                sector = cliente.get("sector", "")
                proceso_prio = cliente.get("proceso_prioritario", "")
                if proceso_prio == "Otro" and cliente.get("proceso_prioritario_otro"):
                    proceso_prio = f"Otro ({cliente.get('proceso_prioritario_otro')})"
                valor_esp = cliente.get("valor_esperado", "")
                nivel = cliente.get("nivel_madurez", "Nivel 1: Inicial / Disperso")
                score = cliente.get("score_global", 0.0)

                matriz = MATRIZ_EVALUACION.get(nivel, MATRIZ_EVALUACION["Nivel 1: Inicial / Disperso"])

                st.markdown(f"""
                <div style="background: white; border: 1px solid #CBD5E1; border-top: 5px solid #0284C7; border-radius: 12px; padding: 24px; margin-top: 15px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 16px;">
                        <div>
                            <span style="font-size: 12px; font-weight: 700; color: #0284C7; text-transform: uppercase;">PROPUESTA DE IMPLEMENTACIÓN BI</span>
                            <h2 style="margin: 4px 0 0 0; color: #0F172A; font-size: 22px;">{empresa}</h2>
                            <div style="color: #64748B; font-size: 13.5px;">Atención: <strong>{responsable}</strong> {f'({rol})' if rol else ''}</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="background: {matriz['bg_color']}; color: {matriz['badge_color']}; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 13px;">
                                {nivel} ({score} pts)
                            </span>
                        </div>
                    </div>

                    <h4 style="color: #0F172A; margin-bottom: 8px;">1. Objetivo y Alcance Recomendado</h4>
                    <p style="color: #334155; font-size: 14px; line-height: 1.5;">
                        A partir del diagnóstico inicial de madurez de datos realizado, <strong>I+S Data Solutions</strong> propone el despliegue del siguiente plan de acción enfocado en <strong>{proceso_prio}</strong>:
                    </p>
                    <div style="background: #F8FAFC; border-left: 4px solid #10B981; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px;">
                        <strong style="color: #065F46; font-size: 14px;">Solución Específica a Implementar:</strong>
                        <p style="margin: 4px 0 0 0; color: #047857; font-size: 14px;">{matriz['solucion']}</p>
                    </div>

                    <h4 style="color: #0F172A; margin-bottom: 8px;">2. Retorno Esperado para {empresa}</h4>
                    <p style="color: #334155; font-size: 14px; line-height: 1.5;">
                        La solución brindará como principal impacto: <strong>{valor_esp}</strong>, eliminando los cuellos de botella detectados en el relevamiento inicial.
                    </p>

                    <h4 style="color: #0F172A; margin-bottom: 8px;">3. Fases de Ejecución:</h4>
                    <ol style="color: #334155; font-size: 13.5px; line-height: 1.6; padding-left: 20px;">
                        {''.join([f'<li style="margin-bottom: 4px;"><strong>{p}</strong></li>' for p in matriz['prioridades_clave']])}
                    </ol>
                </div>
                """, unsafe_allow_html=True)

                texto_propuesta = f"""PROPUESTA DE IMPLEMENTACIÓN DE BUSINESS INTELLIGENCE
I+S DATA SOLUTIONS — Inteligencia de Datos para Decisiones Estratégicas
========================================================================

CLIENTE: {empresa}
ATENCIÓN: {responsable} ({rol})
SECTOR: {sector}
DIAGNÓSTICO: {nivel} (Score: {score}/100)

1. ENFOQUE Y ALCANCE:
Implementación de un sistema de tableros de control y analítica focalizado en el proceso de:
>> {proceso_prio} <<

2. SOLUCIÓN TÉCNICA PROPUESTA:
{matriz['solucion']}

3. RETORNO Y VALOR ESPERADO:
{valor_esp}

4. FASES DEL PLAN DE ACCIÓN:
""" + "\n".join([f"  Paso {i+1}: {p}" for i, p in enumerate(matriz['prioridades_clave'])]) + f"""

5. CONTACTO Y SEGUIMIENTO:
I+S DATA SOLUTIONS
Ubicación: E. Carriego N° 431, La Rioja, Argentina.
========================================================================
"""

                st.download_button(
                    label="📥 Descargar Propuesta Personalizada (.txt)",
                    data=texto_propuesta,
                    file_name=f"propuesta_bi_{empresa.replace(' ', '_').lower()}.txt",
                    mime="text/plain",
                    type="primary"
                )
