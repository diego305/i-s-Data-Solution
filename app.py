"""
Aplicación Principal en Streamlit: Diagnóstico de Madurez de Datos & BI
Herramienta ágil y completa para recolectar entrevistas con clientes,
calcular diagnósticos automáticos y administrar los resultados.
"""

import streamlit as st
from config import APP_TITLE, APP_SUBTITLE, MATRIZ_EVALUACION
from database import init_db
from components.form_view import render_form
from components.admin_view import render_admin
from components.analytics_view import render_analytics
from components.proposal_view import render_proposal


def apply_custom_styles():
    """Aplica diseño visual moderno y refinado con CSS."""
    st.markdown("""
    <style>
    /* Tipografía y márgenes generales */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Ocultar barra superior por defecto si es necesario */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Sidebar estilizada con contraste garantizado en modo claro y oscuro */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }

    /* Títulos de las opciones del menú lateral siempre oscuros y legibles */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] div[role="radiogroup"] label div p {
        color: #0F172A !important;
        font-weight: 600 !important;
        font-size: 14.5px !important;
    }

    /* Etiqueta superior del menú lateral */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > label p,
    section[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
        color: #64748B !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin-bottom: 6px !important;
    }

    /* Cada opción del menú con formato de botón tipo tarjeta */
    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 8px 12px !important;
        margin-bottom: 8px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: #F0F9FF !important;
        border-color: #0284C7 !important;
        transform: translateX(3px) !important;
    }

    /* Botones primarios con gradiente sutil */
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: #FFFFFF !important;
        padding: 0.55rem 1.2rem !important;
        box-shadow: 0 2px 4px rgba(2, 132, 199, 0.2) !important;
    }

    /* Tarjetas y métricas */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 14px 18px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    div[data-testid="metric-container"] label {
        color: #64748B !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    /* Inputs y selects limpios */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_methodology():
    """Muestra la explicación de la Matriz Oficial de Evaluación Interna."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #0F172A; font-weight: 700; margin-bottom: 4px;">ℹ️ Matriz Oficial de Evaluación Interna</h2>
        <p style="color: #64748B; font-size: 14.5px; margin: 0;">
            Criterios y soluciones recomendadas según el nivel de madurez analítica identificado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    for nivel, data in MATRIZ_EVALUACION.items():
        color = data["badge_color"]
        st.markdown(f"""
        <div style="background: white; border: 1px solid #E2E8F0; border-left: 6px solid {color}; border-radius: 10px; padding: 20px 24px; margin-bottom: 18px; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <h3 style="margin: 0; color: #0F172A; font-size: 18px; font-weight: 700;">{nivel}</h3>
                <span style="background: {data['bg_color']}; color: {color}; padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 12px;">OFICIAL</span>
            </div>
            <div style="margin-bottom: 12px;">
                <strong style="color: #475569; font-size: 14px;">🔍 Criterio Diagnóstico:</strong>
                <p style="margin: 4px 0 0 0; color: #1E293B; font-size: 14.5px; line-height: 1.5;">{data['criterio']}</p>
            </div>
            <div style="margin-bottom: 12px;">
                <strong style="color: #047857; font-size: 14px;">🚀 Solución Inicial Recomendada:</strong>
                <p style="margin: 4px 0 0 0; color: #065F46; font-size: 14.5px; line-height: 1.5; font-weight: 600;">{data['solucion']}</p>
            </div>
            <div>
                <strong style="color: #64748B; font-size: 13px;">Pasos de Ejecución Sugeridos:</strong>
                <ul style="margin: 6px 0 0 0; padding-left: 20px; color: #334155; font-size: 13.5px;">
                    {''.join([f'<li style="margin-bottom: 3px;">{p}</li>' for p in data['prioridades_clave']])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)


def main():
    # Inicialización de Streamlit
    st.set_page_config(
        page_title="Diagnóstico BI | Entrevista con Cliente",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inicializar Base de Datos SQLite
    init_db()

    # Inyectar estilos personalizados
    apply_custom_styles()

    # Barra lateral de navegación
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 10px 0 20px 0; border-bottom: 1px solid #E2E8F0; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 26px;">📊</span>
                <div>
                    <h3 style="margin: 0; font-size: 17px; font-weight: 800; color: #0F172A;">BI Diagnóstico</h3>
                    <p style="margin: 0; font-size: 12px; color: #64748B;">Relevamiento con Clientes</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        menu = st.radio(
            "Módulos:",
            [
                "📝 Nueva Entrevista",
                "💼 Propuesta de Trabajo",
                "📋 Panel de Administración",
                "📊 Analítica de Clientes",
                "ℹ️ Matriz & Metodología"
            ],
            index=0
        )

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: #F1F5F9; border-radius: 8px; padding: 12px; font-size: 12px; color: #475569; border: 1px solid #E2E8F0;">
            <strong>💡 Modos de Uso:</strong>
            <ul style="padding-left: 16px; margin: 6px 0 0 0;">
                <li>En vivo durante llamada / reunión con cliente.</li>
                <li>Compartido como formulario de evaluación previa.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Enrutamiento de Módulos
    if menu == "📝 Nueva Entrevista":
        render_form()
    elif menu == "💼 Propuesta de Trabajo":
        render_proposal()
    elif menu == "📋 Panel de Administración":
        render_admin()
    elif menu == "📊 Analítica de Clientes":
        render_analytics()
    elif menu == "ℹ️ Matriz & Metodología":
        render_methodology()


if __name__ == "__main__":
    main()
