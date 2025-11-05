from src.web.services import stage_service
from flask import Blueprint, jsonify

stage_bp = Blueprint("stage", __name__)

@stage_bp.get("/v1/get_stages_project/<int:project_id>")
def get_stages_project(project_id: int):
    """
    Obtiene las etapas asociadas a un proyecto.
    """
    response = stage_service.get_stages_project(project_id)
    if not response:
        return jsonify({"message": "No hay etapas disponibles para este proyecto."}), 404
    return jsonify(response), 200


@stage_bp.get("/v1/get_all_stages")
def get_all_stages():
    """
    Obtiene todas las etapas de todos los proyectos.
    """
    response = stage_service.get_all_stages_by_project()
    if not response:
        return jsonify({"message": "No hay etapas disponibles."}), 404
    return jsonify(response), 200


@stage_bp.patch("/v1/cover_stage/<int:stage_id>")
def cover_stage_by_id(stage_id: int):
    """
    Endpoint para cubrir una etapa específica según su ID.
    """
    result = stage_service.cover_stage(stage_id)
    if result:
        return jsonify({"message": f"La etapa con ID {stage_id} ha pasado de pendiente a en ejecucion exitosamente."}), 200
    return jsonify({"message": f"No se pudo cubrir la etapa con ID {stage_id}. Es posible que ya este en progreso o haya sido cubierta."}), 400