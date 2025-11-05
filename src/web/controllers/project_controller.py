from flask import Blueprint, jsonify, request
from src.web.services import project_service
from werkzeug.exceptions import BadRequest

project_bp = Blueprint("projects", __name__, url_prefix="/projects")

@project_bp.get("/v1/get_projects_with_stages")
def get_projects_with_stages():
    """
    Devuelve todos los proyectos con todas sus etapas.
    """
    result = project_service.list_projects_with_stages()
    return jsonify(result)


@project_bp.post("/v1/add_observation/<int:project_id>")
def add_observation(project_id: int):
    """
    Agrega una observación a un proyecto a partir de su ID de proyecto.
    """
    data = request.get_json()

    try:
        observation = project_service.add_observation(project_id, data)
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {str(e)}"}), 500
    return jsonify({
        "message": f"Observación '{observation.name}' agregada correctamente al proyecto {project_id}.",
        "observation": observation.to_dict()
    }), 201


@project_bp.patch("/v1/upload_corrected_observation/<int:observation_id>")
def upload_corrected_observation(observation_id: int):
    """
    Marcar una observación como completada a partir de su ID.
    """
    observation = project_service.upload_corrected_observation(observation_id)

    if not observation:
        return jsonify({"message": f"No se encontró la observación con ID {observation_id}"}), 404
    return jsonify({"message": f"La observación con ID {observation.id} ha sido marcada como completada."}), 200