"""
Lógica de cálculo de madurez analítica y diagnóstico para la entrevista de BI.
Implementa las reglas de la Matriz Interna de Evaluación.
"""

from typing import Dict, Any, List
from config import MATRIZ_EVALUACION


def calcular_puntaje_almacenamiento(fuentes: List[str]) -> float:
    """Calcula el puntaje de la dimensión de almacenamiento (0-100)."""
    if not fuentes:
        return 20.0
    
    score = 0.0
    tiene_papel = any("papel" in f.lower() for f in fuentes)
    tiene_planillas = any("planillas" in f.lower() for f in fuentes)
    tiene_erp = any("erp" in f.lower() or "tango" in f.lower() for f in fuentes)
    tiene_facturacion = any("facturación" in f.lower() for f in fuentes)
    tiene_crm = any("crm" in f.lower() for f in fuentes)

    if tiene_erp and tiene_crm and not tiene_papel:
        score = 95.0
    elif tiene_erp and (tiene_facturacion or tiene_planillas):
        score = 75.0
    elif tiene_erp:
        score = 70.0
    elif tiene_facturacion and tiene_planillas and not tiene_papel:
        score = 55.0
    elif tiene_planillas and not tiene_papel:
        score = 40.0
    elif tiene_papel and not tiene_erp:
        score = 20.0
    else:
        score = 35.0

    return min(100.0, max(10.0, score))


def calcular_puntaje_integracion(integracion: str) -> float:
    """Calcula el puntaje de integración según la escala 1-4."""
    if not integracion:
        return 25.0
    if integracion.startswith("1"):
        return 25.0
    elif integracion.startswith("2"):
        return 50.0
    elif integracion.startswith("3"):
        return 75.0
    elif integracion.startswith("4"):
        return 100.0
    return 50.0


def calcular_puntaje_frecuencia(frecuencia: str) -> float:
    """Calcula el puntaje de frecuencia de actualización."""
    if not frecuencia:
        return 25.0
    if "Tiempo real" in frecuencia:
        return 100.0
    elif "Semanal" in frecuencia:
        return 75.0
    elif "Mensual" in frecuencia:
        return 50.0
    elif "Eventual" in frecuencia:
        return 25.0
    return 40.0


def calcular_puntaje_calidad(calidad: str) -> float:
    """Calcula el puntaje de calidad y consistencia."""
    if not calidad:
        return 25.0
    if "Alto" in calidad:
        return 100.0
    elif "Medio" in calidad:
        return 65.0
    elif "Bajo" in calidad:
        return 25.0
    return 40.0


def calcular_puntaje_eficiencia(tiempo_reporte: str, herramienta: str) -> float:
    """Calcula el puntaje de reportabilidad y visualización."""
    # Score por tiempo
    s_tiempo = 30.0
    if "minutos de forma automática" in tiempo_reporte:
        s_tiempo = 100.0
    elif "Medio día" in tiempo_reporte:
        s_tiempo = 65.0
    elif "Horas o días" in tiempo_reporte:
        s_tiempo = 35.0
    elif "No contamos" in tiempo_reporte:
        s_tiempo = 20.0

    # Score por herramienta
    s_herr = 30.0
    if "Herramientas de BI" in herramienta:
        s_herr = 100.0
    elif "Informes nativos del ERP" in herramienta:
        s_herr = 75.0
    elif "Planillas de Excel" in herramienta:
        s_herr = 50.0
    elif "Reportes estáticos" in herramienta:
        s_herr = 35.0
    elif "Ninguna" in herramienta:
        s_herr = 15.0

    return round((s_tiempo * 0.5) + (s_herr * 0.5), 1)


def evaluar_diagnostico(respuestas: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evalúa todas las respuestas de la entrevista y retorna:
    - Puntaje por dimensión (0-100)
    - Puntaje global ponderado (0-100)
    - Nivel de madurez (Nivel 1, Nivel 2, Nivel 3)
    - Criterio diagnóstico y solución recomendada de la matriz oficial
    - Puntos críticos y recomendaciones personalizadas
    """
    p_almacenamiento = calcular_puntaje_almacenamiento(respuestas.get("storage_sources", []))
    p_integracion = calcular_puntaje_integracion(respuestas.get("integration_level", ""))
    p_frecuencia = calcular_puntaje_frecuencia(respuestas.get("update_frequency", ""))
    p_calidad = calcular_puntaje_calidad(respuestas.get("data_confidence", ""))
    p_eficiencia = calcular_puntaje_eficiencia(
        respuestas.get("report_time", ""),
        respuestas.get("current_bi_tool", "")
    )

    # Ponderaciones estratégicas
    # Almacenamiento: 20%, Integración: 25%, Frecuencia: 15%, Calidad: 20%, Eficiencia: 20%
    score_global = round(
        (p_almacenamiento * 0.20) +
        (p_integracion * 0.25) +
        (p_frecuencia * 0.15) +
        (p_calidad * 0.20) +
        (p_eficiencia * 0.20),
        1
    )

    # Clasificación en base a la Matriz Interna
    if score_global < 45.0:
        nivel = "Nivel 1: Inicial / Disperso"
    elif score_global < 75.0:
        nivel = "Nivel 2: Operativo / Estructurado"
    else:
        nivel = "Nivel 3: Avanzado / Preparado"

    info_matriz = MATRIZ_EVALUACION[nivel]

    dimensiones = {
        "Almacenamiento y Fuentes": p_almacenamiento,
        "Integración entre Áreas": p_integracion,
        "Frecuencia de Actualización": p_frecuencia,
        "Calidad y Consistencia": p_calidad,
        "Eficiencia de Reportes": p_eficiencia
    }

    return {
        "score_global": score_global,
        "nivel": nivel,
        "criterio": info_matriz["criterio"],
        "solucion_recomendada": info_matriz["solucion"],
        "badge_color": info_matriz["badge_color"],
        "bg_color": info_matriz["bg_color"],
        "prioridades_clave": info_matriz["prioridades_clave"],
        "dimensiones": dimensiones
    }
