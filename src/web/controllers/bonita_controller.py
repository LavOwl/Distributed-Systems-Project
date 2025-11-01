#type: ignore
from pydantic import ValidationError
from flask import Blueprint, request, jsonify
from src.web.services.bonita_service import BonitaService
from src.core.project.services import create_project, set_case_id
from src.core.validators.project import ProjectValidator
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
    #name = payload.get("title", "")
    #escription = payload.get("description", "")

    # Extrae y transforma las etapas.
    # stages = [
    #     {
    #         "name": t.get("name", ""),
    #         "start_date": t.get("startDate", ""),
    #         "end_date": t.get("endDate"),
    #         "coverage_request": t.get("coverageRequest", ""),
    #         "requires_contributor": t.get("requiresContributor", "")
    #     }
    #     for t in payload.get("tasks", [])
    # ]
    try:
        project_in = ProjectValidator.model_validate(payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400


    # Crea el proyecto y sus stages en la base de datos.
    #project = create_project(name, description, stages)

    name = project_in.title
    description = project_in.description or ""

    # Convertir etapas validadas a dicts (model_dump -> dict simple)
    stages = [stage.model_dump() for stage in project_in.stages]

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



@bonita_bp.post("/v1/login")
def bonita_login():
    """
    Realiza el login en Bonita y devuelve un mensaje de éxito o error.
    """
    # Recibe el JSON del body.
    data = request.get_json(silent=True) or {}
    
    bonita = BonitaService()
    if bonita.bonita_login(data):
        return jsonify({"message": "Login en Bonita exitoso."}), 201
    else:
        return jsonify({"error": "No se pudo autenticar en Bonita"}), 500
