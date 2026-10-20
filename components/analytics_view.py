"""
Módulo de Analítica y Estadísticas Globales del Diagnóstico.
Muestra gráficos consolidados del portafolio de clientes entrevistados.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from database import get_all_interviews, seed_sample_data


def render_analytics():
    """Renderiza el panel de inteligencia de datos sobre las entrevistas realizadas."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #0F172A; font-weight: 700; margin-bottom: 4px;">📊 Analítica de Clientes Relevados</h2>
        <p style="color: #64748B; font-size: 14.5px; margin: 0;">
            Visión panorámica de la madurez de datos, cuellos de botella más comunes y procesos prioritarios del mercado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    df = get_all_interviews()
    if df.empty:
        st.info("ℹ️ No hay datos suficientes para calcular analíticas.")
        if st.button("🌱 Cargar Entrevistas de Ejemplo", type="primary"):
            seed_sample_data()
            st.rerun()
        return

    # Tarjetas de Resumen
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Entrevistas", len(df))
    with col2:
        st.metric("Score Promedio", f"{df['score_global'].mean():.1f} pts")
    with col3:
        st.metric("Score Máximo", f"{df['score_global'].max():.1f} pts")
    with col4:
        st.metric("Score Mínimo", f"{df['score_global'].min():.1f} pts")

    st.markdown("---")

    # Fila 1: Distribución por Nivel de Madurez y Sectores
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Distribución de Madurez de Datos")
        conteo_nivel = df["nivel_madurez"].value_counts().reset_index()
        conteo_nivel.columns = ["Nivel", "Cantidad"]

        colores = {
            "Nivel 1: Inicial / Disperso": "#EF4444",
            "Nivel 2: Operativo / Estructurado": "#F59E0B",
            "Nivel 3: Avanzado / Preparado": "#10B981"
        }

        fig_pie = px.pie(
            conteo_nivel,
            names="Nivel",
            values="Cantidad",
            hole=0.45,
            color="Nivel",
            color_discrete_map=colores
        )
        fig_pie.update_layout(margin=dict(l=10, r=10, t=20, b=10), height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.subheader("Entrevistas por Sector Económico")
        conteo_sector = df["sector"].value_counts().reset_index()
        conteo_sector.columns = ["Sector", "Cantidad"]
        fig_sec = px.bar(
            conteo_sector,
            x="Cantidad",
            y="Sector",
            orientation="h",
            color="Sector",
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_sec.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            height=300,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig_sec, use_container_width=True)

    st.markdown("---")

    # Fila 2: Obstáculos Más Frecuentes y Procesos Prioritarios
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Obstáculos Principales para Decidir")
        # Parsear listas de obstaculos
        todos_obstaculos = []
        for raw in df["obstaculos_decision"].dropna():
            try:
                obs_items = json.loads(raw)
                todos_obstaculos.extend(obs_items)
            except Exception:
                pass

        if todos_obstaculos:
            df_obs = pd.Series(todos_obstaculos).value_counts().reset_index()
            df_obs.columns = ["Obstáculo", "Menciones"]
            fig_obs = px.bar(
                df_obs,
                x="Menciones",
                y="Obstáculo",
                orientation="h",
                color="Menciones",
                color_continuous_scale="Reds"
            )
            fig_obs.update_layout(
                margin=dict(l=10, r=10, t=20, b=10),
                height=320,
                yaxis={'categoryorder': 'total ascending'}
            )
            st.plotly_chart(fig_obs, use_container_width=True)
        else:
            st.caption("Sin obstáculos registrados.")

    with c4:
        st.subheader("Procesos Prioritarios para Tablero")
        conteo_proc = df["proceso_prioritario"].value_counts().reset_index()
        conteo_proc.columns = ["Proceso", "Clientes"]
        fig_proc = px.bar(
            conteo_proc,
            x="Proceso",
            y="Clientes",
            color="Proceso",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_proc.update_layout(
            margin=dict(l=10, r=10, t=20, b=10),
            height=320,
            showlegend=False,
            xaxis={'tickangle': -30}
        )
        st.plotly_chart(fig_proc, use_container_width=True)

    # Fila 3: Radar de Madurez Promedio del Portafolio
    st.markdown("---")
    st.subheader("Madurez Promedio de la Cartera por Dimensión")

    # Extraer dimensiones de todos los registros
    dimension_totals = {
        "Almacenamiento y Fuentes": [],
        "Integración entre Áreas": [],
        "Frecuencia de Actualización": [],
        "Calidad y Consistencia": [],
        "Eficiencia de Reportes": []
    }

    for raw in df["dimensiones_json"].dropna():
        try:
            dims = json.loads(raw)
            for k in dimension_totals:
                if k in dims:
                    dimension_totals[k].append(dims[k])
        except Exception:
            pass

    dims_avg = {k: sum(v)/len(v) if v else 50.0 for k, v in dimension_totals.items()}
    cats = list(dims_avg.keys()) + [list(dims_avg.keys())[0]]
    vals = list(dims_avg.values()) + [list(dims_avg.values())[0]]

    fig_avg_radar = go.Figure()
    fig_avg_radar.add_trace(go.Scatterpolar(
        r=vals,
        theta=cats,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.25)',
        line=dict(color='#6366F1', width=3),
        name='Promedio Clientes'
    ))
    fig_avg_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=11)),
        ),
        showlegend=False,
        height=340,
        margin=dict(l=60, r=60, t=30, b=20)
    )
    st.plotly_chart(fig_avg_radar, use_container_width=True)
