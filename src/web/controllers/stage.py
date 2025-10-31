from flask import Blueprint, request, jsonify
from src.core.validators.project import ProjectValidator
from src.web.services import stage_service
import os

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
    print("RESPONSE", response)
    if not response:
        return jsonify({"message": "No hay etapas disponibles."}), 404
    return jsonify(response), 200
