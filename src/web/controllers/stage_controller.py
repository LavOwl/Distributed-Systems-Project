from src.web.handlers.helpers import get_authenticated_bonita_service
from src.web.handlers.authentication import require_bonita_auth
from src.web.services import stage_service
from flask import Blueprint, jsonify, g

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
    Endpoint para cubrir una etapa específica según su ID, donde la etapa pasa de PENDING a IN_PROGRESS.
    (1) Recibe (parámetro de la ruta):
        1. stage_id: int
    (2) Devuelve:
        1. 200 - message: la etapa ha pasado de pendiente a en ejecución exitosamente.
        2. 400 - error: no se pudo cubrir la etapa. Es posible que ya este en progreso o haya sido cubierta.
        3. 401 - error: sesión expirada o inválida.
        4. 403 - error: el usuario no tiene permisos para acceder.
    """
    # Obtención del user_id de la sesión actual.
    user_id = g.bonita_user["user_id"]
    
    # Cubrir la etapa en la base de datos local.
    stage = stage_service.cover_stage(user_id, stage_id)
    
    # Cubrir la etapa en la nube.
    response = stage_service.cover_stage_cloud(user_id, stage_id)

    # Obtener el case_id.
    case_id = stage_service.get_case_id_by_stage(stage)

    # Obtención de las cookies de la sesión actual.
    bonita = get_authenticated_bonita_service()

    # Completar la tarea en Bonita.
    bonita.completar_tarea(case_id)
    if response :
        return jsonify({"message": f"La etapa ha pasado de pendiente a en ejecución exitosamente."}), 200
    return jsonify({"error": f"No se pudo cubrir la etapa. Es posible que ya este en progreso o haya sido cubierta."}), 400


@stage_bp.get("/v1/get_in_progress_stages")
@require_bonita_auth("ong_colaborativa")
def get_in_progress_stages():
    """
    Devuelve las etapas en estado "IN_PROGRESS" del usuario autenticado.
    (1) No recibe nada.
    (2) Devuelve:
        1. 200 - listado con las etapas del usuario autenticado en estado "IN_PROGRESS".
        2. 401 - error: sesión expirada o inválida.
        3. 403 - error: el usuario no tiene permisos para acceder.
        4. 500 - error: mensaje de error específico.
    """
    try:
        user_id = g.bonita_user["user_id"]
        stages = stage_service.get_in_progress_stages_for_user(user_id)
        return jsonify(stages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@stage_bp.patch("/v1/finish_stage_by_id/<int:stage_id>")
@require_bonita_auth("ong_colaborativa")
def finish_stage_by_id(stage_id: int):
    """
    Endpoint para finalizar una etapa específica según su ID, 
    donde la etapa pasa de IN_PROGRESS a FINISHED.
    (1) Recibe (parámetro de la ruta):
        1. stage_id: int
    (2) Devuelve:
        1. 200 - message: la etapa ha pasado a finalizada exitosamente.
        2. 400 - error: no se pudo finalizar la etapa. 
        3. 401 - error: sesión expirada o inválida.
        4. 403 - error: el usuario no tiene permisos para acceder.
        5. 409 - error: el proyecto aún no ha comenzado.
    """
    if(stage_service.project_has_started(stage_id)):
        # Finalizar la etapa en la base de datos local.
        stage = stage_service.finish_stage(stage_id)

        # Verificar que exista la etapa.
        if not stage:
            return jsonify({"error": "No se pudo finalizar la etapa. Verifique su estado actual."}), 400

        # Finalizar la etapa en la nube.
        response = stage_service.finish_stage_cloud(stage_id)

        # Obtención de la sesión Bonita autenticada.
        bonita = get_authenticated_bonita_service()
        case_id = stage_service.get_case_id_by_stage(stage)

        # Completa la tarea en Bonita.
        bonita.completar_tarea(case_id)
        return jsonify({"message": "La etapa ha pasado a finalizada exitosamente."}), 200
    return jsonify({"error": "El proyecto aún no ha comenzado."}), 409