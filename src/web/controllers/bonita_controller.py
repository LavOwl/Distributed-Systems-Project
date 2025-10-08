from flask import Blueprint, request, jsonify
from src.web.services.bonita_service import BonitaService
from src.core.project.services import create_project, set_case_id
import os

bonita_bp = Blueprint("APIbonita", __name__)
BONITA_BASE_URL = os.environ.get("BONITA_BASE_URL")

@bonita_bp.post("/v1/iniciar_proyecto")
def iniciar_proyecto():
    """
    Recibe los datos de un proyecto, lo instancia en la base de datos e inicia su ejecución en Bonita.
    """
    
    # Recibe el JSON del body.
    payload = request.get_json(silent=True) or {}

    # Extrae los datos del proyecto.
    name = payload.get("title", "")
    description = payload.get("description", "")

    # Extrae y transforma las etapas.
    stages = [
        {
            "name": t.get("name", ""),
            "start_date": t.get("startDate", ""),
            "end_date": t.get("endDate"),
            "coverage_request": t.get("converageRequest", ""),
            "requires_contributor": t.get("requiresContributor", "")
        }
        for t in payload.get("tasks", [])
    ]

    # Crea el proyecto y sus stages en la base de datos.
    project = create_project(name, description, stages)

    # Realiza el login con Bonita.
    bonita = BonitaService()
    if not bonita.bonita_login():
        return jsonify({"error": "No se pudo autenticar en Bonita"}), 500

    # Inicia el proceso, obtiene el case_id y lo guarda en la tabla de proyecto.
    case_id = bonita.iniciar_proceso("proceso_de_ejecucion")
    set_case_id(project, case_id)

    # Completa la primera tarea pendiente.
    result = bonita.completar_tarea(case_id)

    # Devuelve respuesta final
    return jsonify({"message": "Proyecto creado y proceso de Bonita iniciado correctamente."})