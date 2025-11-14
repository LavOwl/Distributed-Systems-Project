from flask import Blueprint, jsonify
from src.web.services.project_service import get_project_by_case_id, get_latest_stage_end_date
from datetime import datetime
from src.web.handlers.helpers import get_authenticated_bonita_service

monitor_bp = Blueprint("monitor", __name__, url_prefix="/monitor")


@monitor_bp.get("/v1/casos_exitosos_en_termino")
def casos_exitosos_en_termino():
    """
    1. Promedio de casos que finalizan exitosamente en término.
    """
    bonita = get_authenticated_bonita_service()
    
    # Obtener solo casos completados
    cases = bonita.get_archived_cases("proceso_de_ejecucion")
    
    if not cases:
        return jsonify({
            "message": "No hay casos completados aún",
            "total_casos": 0,
            "casos_en_termino": 0,
            "promedio_porcentaje": 0
        }), 200
    
    total_cases = 0
    cases_on_time = 0
    
    for case in cases:
    
        
        total_cases += 1
        case_id = case['id']
        
        try:
            end_date = datetime.fromisoformat(case['end_date'].replace('Z', '+00:00'))
            
            project = get_project_by_case_id(case_id)
            if not project:
                continue
            
            end_date_project = get_latest_stage_end_date(project)

            if end_date_project and end_date <= end_date_project:
                cases_on_time += 1
        
        except Exception as e:
            print(f"Error procesando case {case_id}: {e}")
            continue
    
    promedio = (cases_on_time / total_cases * 100) if total_cases > 0 else 0
    
    return jsonify({
        "total_casos": total_cases,
        "casos_en_termino": cases_on_time,
        "promedio_porcentaje": round(promedio, 2)
    }), 200
