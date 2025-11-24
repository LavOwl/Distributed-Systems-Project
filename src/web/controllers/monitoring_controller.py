from src.web.services.project_service import get_project_by_case_id, get_latest_stage_end_date
from src.web.handlers.helpers import get_authenticated_bonita_service
from src.web.handlers.authentication import require_bonita_auth
from flask import Blueprint, jsonify
from datetime import datetime

monitor_bp = Blueprint("monitor", __name__, url_prefix="/monitor")

@monitor_bp.get("/v1/casos_exitosos_en_termino")
@require_bonita_auth("perfil_gerencial")
def casos_exitosos_en_termino():
    """
    Promedio de casos que finalizan exitosamente en término.
    (1) No recibe nada.
    (2) Devuelve:
        1. 200 - JSON {message: string (opcional), total_casos: integer, casos_en_termino: integer, promedio_porcentaje: integer}.
    """
    bonita = get_authenticated_bonita_service()
    
    # Obtener solo casos completados.
    cases = bonita.get_archived_cases("proceso_de_ejecucion")
    if not cases:
        return jsonify({
            "message": "No hay casos completados aún",
            "total_casos": 0,
            "casos_en_termino": 0,
            "promedio_porcentaje": 0
        }), 200
    
    # Inicialización de las variables.
    total_cases = 0
    cases_on_time = 0
    
    for case in cases:
        total_cases += 1
        case_id = case['sourceObjectId'] # ID del proceso original, el que nosotros seteamos en la BD.
        try:
            end_date = datetime.fromisoformat(case['end_date'].replace('Z', '+00:00'))
            project = get_project_by_case_id(int(case_id))
            if not project:
                continue
            
            # Obtiene la etapa del proyecto que finaliza última de todas.
            end_date_project = get_latest_stage_end_date(project)

            # Incrementa 1 si la fecha de fin del proceso es menor o igual a la de la etapa que finaliza última de todas.
            if end_date_project and end_date <= end_date_project:
                cases_on_time += 1
        except Exception as e:
            continue
    
    # Cálculo del promedio.
    promedio = (cases_on_time / total_cases * 100) if total_cases > 0 else 0
    return jsonify({
        "total_casos": total_cases,
        "casos_en_termino": cases_on_time,
        "promedio_porcentaje": round(promedio, 2)
    }), 200


@monitor_bp.get("/v1/casos_fuera_de_plazo")
@require_bonita_auth("perfil_gerencial")
def casos_fuera_de_plazo():
    """
    Promedio de casos que terminan fuera del plazo establecido.
    (1) No recibe nada.
    (2) Devuelve:
        1. 200 - JSON {message: string (opcional), total_casos: integer, casos_fuera_de_plazo: integer, promedio_porcentaje: integer}.
    """
    bonita = get_authenticated_bonita_service()

    # Obtener solo casos completados.
    cases = bonita.get_archived_cases("proceso_de_ejecucion")
    if not cases:
        return jsonify({
            "message": "No hay casos completados aún",
            "total_casos": 0,
            "casos_fuera_de_plazo": 0,
            "promedio_porcentaje": 0
        }), 200
    
    # Inicialización de las variables.
    total_cases = 0
    cases_out_time = 0
    
    for case in cases:
        total_cases += 1
        case_id = case['sourceObjectId'] # ID del proceso original, el que nosotros seteamos en la BD.
        try:
            end_date = datetime.fromisoformat(case['end_date'].replace('Z', '+00:00'))
            project = get_project_by_case_id(case_id)
            if not project:
                continue
            
            # Obtiene la etapa del proyecto que finaliza última de todas.
            end_date_project = get_latest_stage_end_date(project)

            # Incrementa 1 si la fecha de fin del proceso es mayor a la de la etapa que finaliza última de todas.
            if end_date_project and end_date > end_date_project:
                cases_out_time += 1
        except Exception as e:
            continue
    
    # Cálculo del promedio.
    promedio = (cases_out_time / total_cases * 100) if total_cases > 0 else 0
    return jsonify({
        "total_casos": total_cases,
        "casos_fuera_plazo": cases_out_time,
        "promedio_porcentaje": round(promedio, 2)
    }), 200


@monitor_bp.get("/v1/casos_sin_colaboracion")
@require_bonita_auth("perfil_gerencial")
def casos_sin_colaboracion():
    """
    Promedio de casos que no requieren colaboración de ONGs.
    (1) No recibe nada.
    (2) Devuelve:
        1. 200 - JSON {total_casos: integer, casos_sin_colaboracion: integer, promedio_porcentaje: integer}.
    """
    bonita = get_authenticated_bonita_service()

    # Obtener solo casos completados.
    cases = bonita.get_archived_cases("proceso_de_ejecucion")
    
    # Inicialización de variables.
    total_casos = len(cases)
    casos_sin_colaboracion = 0
    
    for caso in cases:
        case_id = caso['sourceObjectId'] # ID del proceso original, el que nosotros seteamos en la BD.
        
        # Obtener variable numero_etapas del caso, para saber cuántas requieren colaboración.
        numero_etapas = bonita.get_archive_case_variable(case_id, 'numero_etapas')
        if int(numero_etapas) == 0:  # Si es 0, no requirió colaboración.
            casos_sin_colaboracion += 1
    
    # Cálculo del promedio.
    promedio = (casos_sin_colaboracion / total_casos * 100) if total_casos > 0 else 0
    return jsonify({
        "total_casos": total_casos,
        "casos_sin_colaboracion": casos_sin_colaboracion,
        "promedio_porcentaje": round(promedio, 2)
    }), 200