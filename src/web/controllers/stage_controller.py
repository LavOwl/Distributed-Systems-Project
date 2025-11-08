from src.web.handlers.helpers import get_authenticated_bonita_service
from src.web.handlers.authentication import require_bonita_auth
from src.web.services import stage_service
from flask import Blueprint, jsonify

stage_bp = Blueprint("stage", __name__)

@stage_bp.get("/v1/get_stages_project/<int:project_id>")
@require_bonita_auth("ong_colaborativa")
def get_stages_project(project_id: int):
    """
    Obtiene todas las etapas pendientes asociadas a un proyecto.
    (1) Recibe (parámetro en la ruta):
        1. project_id: int
    (2) Devuelve:
        1. 200 - lista de etapas del proyecto.
        2. 401 - error: sesión expirada o inválida.
        3. 403 - error: el usuario no tiene permisos para acceder.
        4. 404 - message: no hay etapas disponibles para este proyecto.
    """
    response = stage_service.get_stages_project(project_id)
    if not response:
        return jsonify({"message": "No hay etapas disponibles para este proyecto."}), 404
    return jsonify(response), 200


@stage_bp.get("/v1/get_all_stages")
@require_bonita_auth("ong_colaborativa")
def get_all_stages():
    """
    Obtiene todas las etapas pendientes de todos los proyectos.
    (1) No recibe nada.
    (2) Devuelve:
        1. 200 - lista de etapas de todos los proyectos.
        2. 401 - error: sesión expirada o inválida.
        3. 403 - error: el usuario no tiene permisos para acceder.
        4. 404 - message: no hay etapas disponibles.
    """
    response = stage_service.get_all_stages_by_project()
    if not response:
        return jsonify({"message": "No hay etapas disponibles."}), 404
    return jsonify(response), 200


@stage_bp.patch("/v1/cover_stage_by_id/<int:stage_id>")
@require_bonita_auth("ong_colaborativa")
def cover_stage_by_id(stage_id: int):
    """
    Endpoint para cubrir una etapa específica según su ID.
    (1) Recibe (parámetro de la ruta):
        1. stage_id: int
    (2) Devuelve:
        1. 200 - message: la etapa ha pasado de pendiente a en ejecución exitosamente.
        2. 400 - error: no se pudo cubrir la etapa. Es posible que ya este en progreso o haya sido cubierta.
        3. 401 - error: sesión expirada o inválida.
        4. 403 - error: el usuario no tiene permisos para acceder.
    """
    stage = stage_service.cover_stage(stage_id)
    case_id = stage_service.get_case_id_by_stage(stage)

    # Obtención de las cookies de la sesión actual.
    bonita = get_authenticated_bonita_service()

    # Completar la tarea en Bonita.
    bonita.completar_tarea(case_id)
    
    if stage:
        return jsonify({"message": f"La etapa ha pasado de pendiente a en ejecución exitosamente."}), 200
    return jsonify({"error": f"No se pudo cubrir la etapa. Es posible que ya este en progreso o haya sido cubierta."}), 400