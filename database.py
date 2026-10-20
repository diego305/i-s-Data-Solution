"""
Capa de persistencia con SQLite para las entrevistas de diagnóstico de BI.
Proporciona operaciones CRUD completas y exportación.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "entrevistas_bi.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa la base de datos y crea la tabla si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entrevistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            entrevistador TEXT,
            responsable_nombre TEXT NOT NULL,
            responsable_rol TEXT,
            empresa TEXT NOT NULL,
            sector TEXT,
            sector_otro TEXT,
            colaboradores TEXT,
            almacenamiento_fuentes TEXT,
            almacenamiento_otro TEXT,
            integracion_nivel TEXT,
            frecuencia_actualizacion TEXT,
            confianza_datos TEXT,
            tiempo_reporte TEXT,
            herramienta_visualizacion TEXT,
            obstaculos_decision TEXT,
            proceso_prioritario TEXT,
            proceso_prioritario_otro TEXT,
            valor_esperado TEXT,
            observaciones_consultor TEXT,
            score_global REAL,
            nivel_madurez TEXT,
            dimensiones_json TEXT,
            estado TEXT DEFAULT 'Completada'
        )
    """)
    conn.commit()
    conn.close()


def save_interview(data: Dict[str, Any]) -> int:
    """Guarda una nueva entrevista y retorna el ID insertado."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fuentes_json = json.dumps(data.get("storage_sources", []), ensure_ascii=False)
    obstaculos_json = json.dumps(data.get("decision_obstacles", []), ensure_ascii=False)
    dimensiones_json = json.dumps(data.get("dimension_scores", {}), ensure_ascii=False)

    cursor.execute("""
        INSERT INTO entrevistas (
            created_at, updated_at, entrevistador, responsable_nombre, responsable_rol,
            empresa, sector, sector_otro, colaboradores, almacenamiento_fuentes,
            almacenamiento_otro, integracion_nivel, frecuencia_actualizacion,
            confianza_datos, tiempo_reporte, herramienta_visualizacion,
            obstaculos_decision, proceso_prioritario, proceso_prioritario_otro,
            valor_esperado, observaciones_consultor, score_global, nivel_madurez,
            dimensiones_json, estado
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        now, now,
        data.get("interviewer", ""),
        data.get("interviewee_name", ""),
        data.get("role", ""),
        data.get("company", ""),
        data.get("sector", ""),
        data.get("sector_other", ""),
        data.get("employee_count", ""),
        fuentes_json,
        data.get("storage_other", ""),
        data.get("integration_level", ""),
        data.get("update_frequency", ""),
        data.get("data_confidence", ""),
        data.get("report_time", ""),
        data.get("current_bi_tool", ""),
        obstaculos_json,
        data.get("priority_process", ""),
        data.get("priority_other", ""),
        data.get("expected_value", ""),
        data.get("consultant_notes", ""),
        float(data.get("maturity_score", 0.0)),
        data.get("maturity_level", "Nivel 1: Inicial / Disperso"),
        dimensiones_json,
        data.get("status", "Completada")
    ))

    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_interview(interview_id: int, data: Dict[str, Any]) -> bool:
    """Actualiza una entrevista existente por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fuentes_json = json.dumps(data.get("storage_sources", []), ensure_ascii=False)
    obstaculos_json = json.dumps(data.get("decision_obstacles", []), ensure_ascii=False)
    dimensiones_json = json.dumps(data.get("dimension_scores", {}), ensure_ascii=False)

    cursor.execute("""
        UPDATE entrevistas SET
            updated_at = ?,
            entrevistador = ?,
            responsable_nombre = ?,
            responsable_rol = ?,
            empresa = ?,
            sector = ?,
            sector_otro = ?,
            colaboradores = ?,
            almacenamiento_fuentes = ?,
            almacenamiento_otro = ?,
            integracion_nivel = ?,
            frecuencia_actualizacion = ?,
            confianza_datos = ?,
            tiempo_reporte = ?,
            herramienta_visualizacion = ?,
            obstaculos_decision = ?,
            proceso_prioritario = ?,
            proceso_prioritario_otro = ?,
            valor_esperado = ?,
            observaciones_consultor = ?,
            score_global = ?,
            nivel_madurez = ?,
            dimensiones_json = ?,
            estado = ?
        WHERE id = ?
    """, (
        now,
        data.get("interviewer", ""),
        data.get("interviewee_name", ""),
        data.get("role", ""),
        data.get("company", ""),
        data.get("sector", ""),
        data.get("sector_other", ""),
        data.get("employee_count", ""),
        fuentes_json,
        data.get("storage_other", ""),
        data.get("integration_level", ""),
        data.get("update_frequency", ""),
        data.get("data_confidence", ""),
        data.get("report_time", ""),
        data.get("current_bi_tool", ""),
        obstaculos_json,
        data.get("priority_process", ""),
        data.get("priority_other", ""),
        data.get("expected_value", ""),
        data.get("consultant_notes", ""),
        float(data.get("maturity_score", 0.0)),
        data.get("maturity_level", "Nivel 1: Inicial / Disperso"),
        dimensiones_json,
        data.get("status", "Completada"),
        interview_id
    ))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def delete_interview(interview_id: int) -> bool:
    """Elimina una entrevista por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entrevistas WHERE id = ?", (interview_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def get_interview(interview_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene una entrevista individual con campos parseados."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entrevistas WHERE id = ?", (interview_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    item = dict(row)
    try:
        item["almacenamiento_fuentes_list"] = json.loads(item.get("almacenamiento_fuentes") or "[]")
    except Exception:
        item["almacenamiento_fuentes_list"] = []

    try:
        item["obstaculos_decision_list"] = json.loads(item.get("obstaculos_decision") or "[]")
    except Exception:
        item["obstaculos_decision_list"] = []

    try:
        item["dimensiones_dict"] = json.loads(item.get("dimensiones_json") or "{}")
    except Exception:
        item["dimensiones_dict"] = {}

    return item


def get_all_interviews() -> pd.DataFrame:
    """Retorna todas las entrevistas en formato DataFrame para análisis y administración."""
    init_db()
    conn = get_connection()
    query = "SELECT * FROM entrevistas ORDER BY created_at DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def seed_sample_data():
    """Genera datos de prueba representativos para cada nivel de madurez."""
    from scoring import evaluar_diagnostico
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM entrevistas")
    count = cursor.fetchone()[0]
    conn.close()

    if count > 0:
        return  # Ya hay datos

    muestras = [
        {
            "interviewer": "Consultor Senior BI",
            "interviewee_name": "Martín Rodríguez",
            "role": "Gerente General",
            "company": "Finca Los Olivos S.A.",
            "sector": "Agroindustria / Olivícola",
            "sector_other": "",
            "employee_count": "11 a 50",
            "storage_sources": [
                "Planillas de cálculo (Excel, Google Sheets) en carpetas locales o compartidas",
                "Documentos en papel / cuadernos de registro diario"
            ],
            "storage_other": "",
            "integration_level": "1 - Muy fragmentada: Cada área maneja sus propios archivos y no coinciden entre sí.",
            "update_frequency": "Eventual / solo cuando se necesita un informe puntual",
            "data_confidence": "Bajo: Solemos encontrar duplicados, errores de carga o números que no cierran.",
            "report_time": "Horas o días de trabajo manual recopilando y cruzando planillas.",
            "current_bi_tool": "Planillas de Excel / tablas dinámicas",
            "decision_obstacles": [
                "Demora en obtener números actualizados.",
                "Discrepancias entre los datos de distintos departamentos.",
                "Dependencia excesiva de una persona clave para armar los reportes."
            ],
            "priority_process": "Ventas, cobranzas y margen comercial",
            "priority_other": "",
            "expected_value": "Ahorro de tiempo operativo en el armado de informes.",
            "consultant_notes": "Gran interés en centralizar costos de cosecha y agilizar cobranzas. Fuertemente dependientes de cuadernos en el campo.",
            "status": "Completada"
        },
        {
            "interviewer": "Consultor Senior BI",
            "interviewee_name": "Valeria Gómez",
            "role": "Directora de Operaciones",
            "company": "Distribuidora Cuyo Express",
            "sector": "Comercio mayorista / minorista",
            "sector_other": "",
            "employee_count": "51 a 200",
            "storage_sources": [
                "Planillas de cálculo (Excel, Google Sheets) en carpetas locales o compartidas",
                "Software de gestión o ERP (Tango, Bejerman, SAP, Odoo, sistema a medida, etc.)",
                "Sistema de facturación electrónica o comprobantes fiscales"
            ],
            "storage_other": "",
            "integration_level": "2 - Básica: Hay sistemas distintos y cruzamos datos manualmente a fin de mes.",
            "update_frequency": "Semanal",
            "data_confidence": "Medio: Los datos son confiables pero requieren revisión y limpieza manual previa.",
            "report_time": "Medio día, con plantillas prearmadas pero manuales.",
            "current_bi_tool": "Informes nativos del ERP / software contable",
            "decision_obstacles": [
                "Demora en obtener números actualizados.",
                "Dificultad para visualizar tendencias o anomalías a tiempo."
            ],
            "priority_process": "Control de stock, inventario y compras",
            "priority_other": "",
            "expected_value": "Visibilidad ejecutiva en tiempo real accesible desde el celular o la web.",
            "consultant_notes": "Tienen ERP Tango pero el control de stock real se termina conciliando en Excel por quiebres de inventario.",
            "status": "Completada"
        },
        {
            "interviewer": "Consultor Senior BI",
            "interviewee_name": "Carlos Méndez",
            "role": "CFO / Director de Finanzas",
            "company": "Andes Logística Global",
            "sector": "Logística / Distribución",
            "sector_other": "",
            "employee_count": "Más de 200",
            "storage_sources": [
                "Software de gestión o ERP (Tango, Bejerman, SAP, Odoo, sistema a medida, etc.)",
                "Sistema de facturación electrónica o comprobantes fiscales",
                "CRM o plataformas de ventas / e-commerce"
            ],
            "storage_other": "",
            "integration_level": "3 - Parcialmente integrada: Usamos un sistema central pero con muchas planillas auxiliares.",
            "update_frequency": "Tiempo real / diaria",
            "data_confidence": "Alto: Los registros son consistentes, estandarizados y auditados periódicamente.",
            "report_time": "Se obtienen en minutos de forma automática.",
            "current_bi_tool": "Herramientas de BI (Power BI, Looker Studio, Tableau)",
            "decision_obstacles": [
                "Falta de claridad o acuerdo sobre cuáles son los KPIs prioritarios.",
                "Dificultad para visualizar tendencias o anomalías a tiempo."
            ],
            "priority_process": "Flujo de caja (cash flow) y costos",
            "priority_other": "",
            "expected_value": "Anticipar desvíos antes del cierre mensual.",
            "consultant_notes": "Cuentan con Power BI con métricas básicas de ventas pero necesitan modelar el flujo de caja operativo y predictibilidad de flota.",
            "status": "Completada"
        }
    ]

    for m in muestras:
        diag = evaluar_diagnostico(m)
        m["maturity_score"] = diag["score_global"]
        m["maturity_level"] = diag["nivel"]
        m["dimension_scores"] = diag["dimensiones"]
        save_interview(m)
