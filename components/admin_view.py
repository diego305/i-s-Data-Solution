"""
Panel de Administración de Entrevistas.
Permite visualizar, filtrar, buscar, exportar (Excel/CSV/JSON), inspeccionar y eliminar entrevistas.
"""

import streamlit as st
import pandas as pd
import io
import json
from database import get_all_interviews, delete_interview, get_interview, update_interview, seed_sample_data
from components.report_view import render_report


def render_admin():
    """Renderiza la vista de administración completa."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #0F172A; font-weight: 700; margin-bottom: 4px;">📋 Panel de Administración de Entrevistas</h2>
        <p style="color: #64748B; font-size: 14.5px; margin: 0;">
            Gestione todos los relevamientos realizados, exporte la base consolidada y consulte los informes de cada cliente.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Revisar si se seleccionó ver el informe de un cliente específico
    if "admin_view_id" in st.session_state and st.session_state["admin_view_id"] is not None:
        entrevista_id = st.session_state["admin_view_id"]
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("⬅️ Volver al Listado", type="secondary"):
                st.session_state["admin_view_id"] = None
                st.rerun()
        
        entrevista_sel = get_interview(entrevista_id)
        if entrevista_sel:
            render_report(entrevista_sel)
        else:
            st.error("No se encontró la entrevista seleccionada.")
        return

    # Obtener datos de la base SQLite
    df = get_all_interviews()

    # Si está vacía, ofrecer cargar datos muestra
    if df.empty:
        st.info("ℹ️ Todavía no hay entrevistas registradas en la base de datos.")
        if st.button("🌱 Cargar Entrevistas de Ejemplo (Demo)", type="primary"):
            seed_sample_data()
            st.success("Se cargaron 3 entrevistas de prueba representativas de cada nivel.")
            st.rerun()
        return

    # Métricas directivas arriba
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Total Entrevistas", len(df))
    with col_m2:
        promedio_score = round(df["score_global"].mean(), 1) if "score_global" in df.columns else 0.0
        st.metric("Score Promedio", f"{promedio_score} / 100")
    with col_m3:
        top_sector = df["sector"].mode()[0] if not df["sector"].empty else "N/A"
        st.metric("Sector Principal", top_sector)
    with col_m4:
        top_nivel = df["nivel_madurez"].mode()[0] if not df["nivel_madurez"].empty else "N/A"
        # Simplificar nombre para la card
        nivel_corto = top_nivel.split(":")[0] if ":" in top_nivel else top_nivel
        st.metric("Nivel Predominante", nivel_corto)

    st.markdown("---")

    # Filtros y Búsqueda
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        busqueda = st.text_input("🔍 Buscar por Empresa, Responsable o Consultor:", placeholder="Escriba para filtrar...")
    with col_f2:
        niveles_disp = ["Todos"] + sorted(list(df["nivel_madurez"].dropna().unique()))
        filtro_nivel = st.selectbox("Filtrar por Nivel:", niveles_disp)
    with col_f3:
        sectores_disp = ["Todos"] + sorted(list(df["sector"].dropna().unique()))
        filtro_sector = st.selectbox("Filtrar por Sector:", sectores_disp)

    # Aplicar filtros
    df_filtrado = df.copy()
    if busqueda:
        b = busqueda.lower()
        df_filtrado = df_filtrado[
            df_filtrado["empresa"].str.lower().str.contains(b, na=False) |
            df_filtrado["responsable_nombre"].str.lower().str.contains(b, na=False) |
            df_filtrado["entrevistador"].str.lower().str.contains(b, na=False)
        ]

    if filtro_nivel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["nivel_madurez"] == filtro_nivel]

    if filtro_sector != "Todos":
        df_filtrado = df_filtrado[df_filtrado["sector"] == filtro_sector]

    # Barra de Exportación
    st.markdown(f"**Registros encontrados:** `{len(df_filtrado)}`")
    col_exp1, col_exp2, col_exp3, col_exp4 = st.columns([1, 1, 1, 2])

    with col_exp1:
        # Exportar a Excel
        buffer_excel = io.BytesIO()
        with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
            df_filtrado.to_excel(writer, index=False, sheet_name="Entrevistas_BI")
        st.download_button(
            label="📊 Descargar Excel",
            data=buffer_excel.getvalue(),
            file_name="diagnostico_entrevistas_bi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col_exp2:
        # Exportar a CSV
        csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Descargar CSV",
            data=csv_data,
            file_name="diagnostico_entrevistas_bi.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_exp3:
        # Exportar a JSON
        json_data = df_filtrado.to_json(orient="records", force_ascii=False, indent=2)
        st.download_button(
            label="📦 Descargar JSON",
            data=json_data,
            file_name="diagnostico_entrevistas_bi.json",
            mime="application/json",
            use_container_width=True
        )

    with col_exp4:
        if st.button("🌱 Sembrar Datos de Prueba", help="Agrega 3 entrevistas representativas"):
            seed_sample_data()
            st.rerun()

    # Tabla Visual de Entrevistas
    st.markdown("### Listado de Entrevistas")
    
    # Renderizamos filas con tarjetas interactivas para que sea amigable y directo
    for _, row in df_filtrado.iterrows():
        eid = int(row["id"])
        empresa = row.get("empresa", "")
        responsable = row.get("responsable_nombre", "")
        rol = row.get("responsable_rol", "")
        sector = row.get("sector", "")
        fecha = str(row.get("created_at", ""))[:16]
        score = row.get("score_global", 0.0)
        nivel = row.get("nivel_madurez", "")

        # Color indicator
        color_dot = "#EF4444" if "Nivel 1" in nivel else ("#F59E0B" if "Nivel 2" in nivel else "#10B981")

        with st.container():
            st.markdown(f"""
            <div style="background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px 18px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <span style="height: 12px; width: 12px; background-color: {color_dot}; border-radius: 50%; display: inline-block;"></span>
                    <div>
                        <strong style="color: #0F172A; font-size: 16px;">{empresa}</strong>
                        <div style="color: #64748B; font-size: 13px;">
                            {responsable} {f'({rol})' if rol else ''} • {sector} • 📅 {fecha}
                        </div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span style="background: rgba(15,23,42,0.06); padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 13px; color: #0F172A;">
                        Score: {score} pts
                    </span>
                    <div style="font-size: 12px; color: {color_dot}; font-weight: 600; margin-top: 3px;">
                        {nivel}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_a1, col_a2, col_a3, _ = st.columns([1.5, 1.5, 1, 4])
            with col_a1:
                if st.button(f"👁️ Ver Informe", key=f"ver_{eid}", use_container_width=True):
                    st.session_state["admin_view_id"] = eid
                    st.rerun()

            with col_a2:
                with st.popover(f"✏️ Editar Notas #{eid}"):
                    st.markdown(f"**Notas para {empresa}**")
                    nuevas_notas = st.text_area("Observaciones:", value=row.get("observaciones_consultor", "") or "", key=f"edit_note_{eid}")
                    nuevo_estado = st.selectbox("Estado:", ["Completada", "En Seguimiento", "Archivada"], index=0, key=f"edit_st_{eid}")
                    if st.button("Guardar Cambios", key=f"save_edit_{eid}", type="primary"):
                        row_dict = get_interview(eid)
                        if row_dict:
                            row_dict["consultant_notes"] = nuevas_notas
                            row_dict["status"] = nuevo_estado
                            row_dict["storage_sources"] = row_dict.get("almacenamiento_fuentes_list", [])
                            row_dict["decision_obstacles"] = row_dict.get("obstaculos_decision_list", [])
                            row_dict["dimension_scores"] = row_dict.get("dimensiones_dict", {})
                            row_dict["interviewee_name"] = row_dict.get("responsable_nombre", "")
                            row_dict["role"] = row_dict.get("responsable_rol", "")
                            row_dict["interviewer"] = row_dict.get("entrevistador", "")
                            row_dict["employee_count"] = row_dict.get("colaboradores", "")
                            row_dict["storage_other"] = row_dict.get("almacenamiento_otro", "")
                            row_dict["integration_level"] = row_dict.get("integracion_nivel", "")
                            row_dict["update_frequency"] = row_dict.get("frecuencia_actualizacion", "")
                            row_dict["data_confidence"] = row_dict.get("confianza_datos", "")
                            row_dict["report_time"] = row_dict.get("tiempo_reporte", "")
                            row_dict["current_bi_tool"] = row_dict.get("herramienta_visualizacion", "")
                            row_dict["priority_process"] = row_dict.get("proceso_prioritario", "")
                            row_dict["priority_other"] = row_dict.get("proceso_prioritario_otro", "")
                            row_dict["expected_value"] = row_dict.get("valor_esperado", "")
                            row_dict["maturity_score"] = row_dict.get("score_global", 0.0)
                            row_dict["maturity_level"] = row_dict.get("nivel_madurez", "")
                            update_interview(eid, row_dict)
                            st.success("Actualizado con éxito.")
                            st.rerun()

            with col_a3:
                with st.popover(f"🗑️ Eliminar"):
                    st.warning(f"¿Confirma eliminar la entrevista de '{empresa}'?")
                    if st.button("Sí, Eliminar", key=f"del_{eid}", type="primary"):
                        delete_interview(eid)
                        st.success(f"Entrevista #{eid} eliminada.")
                        st.rerun()

            st.write("")
