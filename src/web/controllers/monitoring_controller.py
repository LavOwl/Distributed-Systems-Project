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
        case_id = case['sourceObjectId'] #Id del proceso original, el que nosotros seteamos en la BD

        try:
            end_date = datetime.fromisoformat(case['end_date'].replace('Z', '+00:00'))
            project = get_project_by_case_id(int(case_id))
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


@monitor_bp.get("/v1/casos_fuera_de_plazo")
def casos_fuera_de_plazo():
    """
     2. Promedio de casos que terminan fuera del plazo establecido.
    """
    bonita = get_authenticated_bonita_service()
    
    cases = bonita.get_archived_cases("proceso_de_ejecucion")
    
    if not cases:
        return jsonify({
            "message": "No hay casos completados aún",
            "total_casos": 0,
            "casos_fuera_de_plazo": 0,
            "promedio_porcentaje": 0
        }), 200
    
    total_cases = 0
    cases_out_time = 0
    
    for case in cases:
    
        
        total_cases += 1
        case_id = case['sourceObjectId']    
        try:
            end_date = datetime.fromisoformat(case['end_date'].replace('Z', '+00:00'))
            
            project = get_project_by_case_id(case_id)
            if not project:
                continue
            
            end_date_project = get_latest_stage_end_date(project)

            # Verificar si terminó fuera de plazo
            if end_date_project and end_date >= end_date_project:
                cases_out_time += 1
        
        except Exception as e:
            print(f"Error procesando case {case_id}: {e}")
            continue
        
        
    promedio = (cases_out_time / total_cases * 100) if total_cases > 0 else 0
   
    return jsonify({
                "total_casos": total_cases,
                "casos_fuera_plazo": cases_out_time,
                "promedio_porcentaje": round(promedio, 2)
            }), 200








# @monitor_bp.get("/v1/tareas_exitosas_colaboradoras")
# def tareas_exitosas_colaboradoras():
#     """
#     2. Listado de tareas ejecutadas exitosamente por ONGs colaboradoras en tiempo y forma.
#     """
    
#     bonita = get_authenticated_bonita_service()
    
#     # Obtener tareas archivadas
#     tareas = bonita.get_archived_tasks()
    
#     # Filtrar solo las de ONGs colaboradoras
#     # Asumiendo que tienen un rol específico
#     tareas_colaboradoras = []
    
#     for tarea in tareas:
#         # Verificar si es de una ONG colaboradora
#         # Esto depende de cómo identifiques a las ONGs colaboradoras
#         if tarea.get('state') == 'completed' and tarea:
#             tareas_colaboradoras.append({
#                 "tarea_nombre": tarea.get('displayName'),
#                 "case_id": tarea.get('caseId'),
#                 "completada_por": tarea.get('assigned_id'),
#                 "fecha_completada": tarea.get('archivedDate')
#             })
    
#     return jsonify({
#         "total_tareas": len(tareas_colaboradoras),
#         "tareas": tareas_colaboradoras[:50]  # Limitar a 50
#     }), 200

@monitor_bp.get("/v1/casos_sin_colaboracion")
def casos_sin_colaboracion():
    """
    3. Promedio de casos que no requieren colaboración de ONGs.
    """
    bonita = get_authenticated_bonita_service()
    
    cases = bonita.get_archived_cases("proceso_de_ejecucion")
    
    total_casos = len(cases)
    casos_sin_colaboracion = 0
    
    for caso in cases:
        case_id = caso['sourceObjectId']
        
        # Obtener variable numero_etapas del caso
        numero_etapas = bonita.get_archive_case_variable(case_id, 'numero_etapas')
        if int(numero_etapas) == 0:  # No requirió colaboración
            casos_sin_colaboracion += 1
    
    promedio = (casos_sin_colaboracion / total_casos * 100) if total_casos > 0 else 0
    
    return jsonify({
        "total_casos": total_casos,
        "casos_sin_colaboracion": casos_sin_colaboracion,
        "promedio_porcentaje": round(promedio, 2)
    }), 200



