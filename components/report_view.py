"""
Componente para visualizar el Informe Ejecutivo de Diagnóstico de BI.
Muestra el nivel de madurez, desglose de dimensiones, gráficos y recomendaciones oficiales.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any
from config import MATRIZ_EVALUACION


def render_report(entrevista: Dict[str, Any], show_back_button: bool = True):
    """Renderiza el informe completo de una entrevista."""
    if not entrevista:
        st.warning("No se encontraron datos para mostrar el informe.")
        return

    # Extraer valores clave
    empresa = entrevista.get("empresa", "Empresa Sin Nombre")
    responsable = entrevista.get("responsable_nombre", "Responsable")
    rol = entrevista.get("responsable_rol", "")
    sector = entrevista.get("sector", "")
    if sector == "Otro" and entrevista.get("sector_other"):
        sector = f"Otro ({entrevista.get('sector_other')})"
    fecha = entrevista.get("created_at", "")[:10]
    score = float(entrevista.get("score_global", 0.0))
    nivel = entrevista.get("nivel_madurez", "Nivel 1: Inicial / Disperso")
    dimensiones = entrevista.get("dimensiones_dict", {})
    obs_list = entrevista.get("obstaculos_decision_list", [])
    fuentes_list = entrevista.get("almacenamiento_fuentes_list", [])
    
    matriz_info = MATRIZ_EVALUACION.get(nivel, MATRIZ_EVALUACION["Nivel 1: Inicial / Disperso"])
    badge_color = matriz_info["badge_color"]

    # Header Card
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 24px 28px; border-radius: 14px; color: #FFFFFF; margin-bottom: 24px; border: 1px solid #334155;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
                <span style="background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 500;">
                    INFORME DE EVALUACIÓN BI • {fecha}
                </span>
                <h1 style="margin: 12px 0 4px 0; font-size: 28px; font-weight: 700; color: #F8FAFC;">{empresa}</h1>
                <p style="margin: 0; color: #94A3B8; font-size: 15px;">
                    Entrevistado: <strong>{responsable}</strong> {f'({rol})' if rol else ''} | Sector: <strong>{sector}</strong>
                </p>
            </div>
            <div style="text-align: right; background: {matriz_info['bg_color']}; border: 1px solid {badge_color}; padding: 12px 20px; border-radius: 12px;">
                <span style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: {badge_color}; font-weight: 600;">Diagnóstico Oficial</span>
                <h3 style="margin: 4px 0 0 0; color: {badge_color}; font-size: 20px; font-weight: 800;">{nivel}</h3>
                <div style="color: #F8FAFC; font-size: 14px; margin-top: 4px;">Puntaje: <strong>{score} / 100</strong></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2 Columnas principales: Gráfico Gauge y Radar de Dimensiones
    col_gauge, col_radar = st.columns([1, 1])

    with col_gauge:
        st.subheader("Índice de Madurez Global")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={'suffix': " pts", 'font': {'size': 36, 'color': '#0F172A'}},
            title={'text': "Nivel de Preparación BI", 'font': {'size': 16, 'color': '#64748B'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#CBD5E1"},
                'bar': {'color': badge_color, 'thickness': 0.28},
                'bgcolor': "white",
                'borderwidth': 1,
                'bordercolor': "#E2E8F0",
                'steps': [
                    {'range': [0, 45], 'color': "rgba(239, 68, 68, 0.15)"},
                    {'range': [45, 75], 'color': "rgba(245, 158, 11, 0.15)"},
                    {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.15)"}
                ],
                'threshold': {
                    'line': {'color': badge_color, 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))
        fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_radar:
        st.subheader("Evaluación por Dimensiones Clave")
        if dimensiones:
            categories = list(dimensiones.keys())
            values = list(dimensiones.values())
            # Cerrar el radar
            categories_closed = categories + [categories[0]]
            values_closed = values + [values[0]]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                fillcolor='rgba(14, 165, 233, 0.25)',
                line=dict(color='#0284C7', width=2),
                name='Madurez'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
                ),
                showlegend=False,
                height=280,
                margin=dict(l=40, r=40, t=30, b=20)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        else:
            st.info("Sin desglose de dimensiones disponible.")

    # Matriz Interna de Evaluación Card (Destacado Oficial del Formulario)
    st.markdown("---")
    st.markdown("### 🎯 Dictamen y Solución Recomendada (Matriz Oficial)")
    
    col_mat1, col_mat2 = st.columns([1, 1])
    with col_mat1:
        st.markdown(f"""
        <div style="background-color: #F8FAFC; border-left: 4px solid {badge_color}; padding: 18px; border-radius: 8px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="margin: 0 0 8px 0; color: #0F172A; font-size: 16px;">🔍 Criterio Diagnóstico</h4>
            <p style="margin: 0; color: #334155; font-size: 14.5px; line-height: 1.5;">{matriz_info['criterio']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_mat2:
        st.markdown(f"""
        <div style="background-color: #F0FDF4; border-left: 4px solid #10B981; padding: 18px; border-radius: 8px; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="margin: 0 0 8px 0; color: #065F46; font-size: 16px;">🚀 Solución Inicial Recomendada</h4>
            <p style="margin: 0; color: #047857; font-size: 14.5px; line-height: 1.5; font-weight: 500;">{matriz_info['solucion']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Prioridades de Implementación
    st.markdown("#### 📋 Plan de Acción y Prioridades Clave:")
    cols_prio = st.columns(len(matriz_info['prioridades_clave']))
    for idx, (col_p, p_text) in enumerate(zip(cols_prio, matriz_info['prioridades_clave'])):
        with col_p:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; height: 100%; border-top: 3px solid #0284C7;">
                <div style="font-weight: 700; color: #0284C7; font-size: 12px; margin-bottom: 4px;">PASO {idx+1}</div>
                <div style="color: #1E293B; font-size: 13px; line-height: 1.4;">{p_text}</div>
            </div>
            """, unsafe_allow_html=True)

    # Detalle de la Entrevista Relevada
    st.markdown("---")
    st.markdown("### 📑 Relevamiento Detallado")

    col_det1, col_det2 = st.columns(2)
    with col_det1:
        st.markdown("**Infraestructura y Datos:**")
        st.markdown(f"- **Integración entre áreas:** {entrevista.get('integracion_nivel', 'N/A')}")
        st.markdown(f"- **Frecuencia de actualización:** {entrevista.get('frecuencia_actualizacion', 'N/A')}")
        st.markdown(f"- **Confianza en los datos:** {entrevista.get('confianza_datos', 'N/A')}")
        st.markdown(f"- **Herramienta actual de análisis:** {entrevista.get('herramienta_visualizacion', 'N/A')}")
        st.markdown(f"- **Tiempo dedicado a armar reportes:** {entrevista.get('tiempo_reporte', 'N/A')}")

        st.markdown("**Fuentes donde se almacena la información:**")
        if fuentes_list:
            for f in fuentes_list:
                st.markdown(f"  • {f}")
        else:
            st.caption("No especificadas")

    with col_det2:
        st.markdown("**Objetivos y Expectativas del Cliente:**")
        proceso_prio = entrevista.get('proceso_prioritario', 'N/A')
        if proceso_prio == "Otro" and entrevista.get('proceso_prioritario_otro'):
            proceso_prio = f"Otro ({entrevista.get('proceso_prioritario_otro')})"
        st.markdown(f"- **Proceso prioritario para tablero:** `{proceso_prio}`")
        st.markdown(f"- **Valor principal esperado:** `{entrevista.get('valor_esperado', 'N/A')}`")

        st.markdown("**Principales obstáculos al tomar decisiones:**")
        if obs_list:
            for obs in obs_list:
                st.markdown(f"  ⚠️ {obs}")
        else:
            st.caption("Ninguno marcado")

        if entrevista.get("observaciones_consultor"):
            st.markdown("**Notas del Consultor / Observaciones:**")
            st.info(entrevista.get("observaciones_consultor"))

    # Exportación / Resumen
    st.markdown("---")
    resumen_txt = f"""# REPORTE DE EVALUACIÓN DE MADUREZ DE DATOS & BI
Empresa: {empresa}
Responsable: {responsable} ({rol})
Sector: {sector}
Fecha: {fecha}
Puntaje Global: {score}/100
Nivel de Madurez: {nivel}

CRITERIO DIAGNÓSTICO:
{matriz_info['criterio']}

SOLUCIÓN INICIAL RECOMENDADA:
{matriz_info['solucion']}

PLAN DE ACCIÓN:
""" + "\n".join([f"- {p}" for p in matriz_info['prioridades_clave']]) + f"""

PROCESO PRIORITARIO: {proceso_prio}
VALOR ESPERADO: {entrevista.get('valor_esperado', 'N/A')}
NOTAS DEL CONSULTOR: {entrevista.get('observaciones_consultor', 'Sin observaciones')}
"""

    st.download_button(
        label="📥 Descargar Informe Resumido (.txt)",
        data=resumen_txt,
        file_name=f"diagnostico_bi_{empresa.replace(' ', '_').lower()}.txt",
        mime="text/plain"
    )
