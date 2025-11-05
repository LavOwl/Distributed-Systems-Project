from src.web.services.bonita_service import BonitaService
from flask import Blueprint, request, jsonify
from src.web.services import project_service
from pydantic import ValidationError
import os

bonita_bp = Blueprint("bonita", __name__)
BONITA_BASE_URL = os.environ.get("BONITA_BASE_URL")

@bonita_bp.post("/v1/iniciar_proyecto")
def iniciar_proyecto():
    """
    Recibe los datos de un proyecto, lo instancia en la base de datos e inicia su ejecución en Bonita.
    """
    # Almacenamiento del payload recibido.
    payload = request.get_json(silent=True) or {}

    # Validar y crear proyecto.
    try:
        project = project_service.create_project_from_payload(payload)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    # Se autentica y ejecutar tarea en Bonita.
    bonita = BonitaService()
    if not bonita.bonita_login(payload):
        return jsonify({"error": "No se pudo autenticar en Bonita"}), 500

    try:
        # Inicia el proceso y lo vincula con el case_id.
        case_id = bonita.iniciar_proceso("proceso_de_ejecucion")
        project_service.link_to_bonita_case(project, case_id)
        
        # Completa la primer tarea pendiente.
        bonita.completar_tarea(case_id)
        
        return jsonify({
            "message": "Proyecto creado y proceso de Bonita iniciado correctamente.",
            "project_id": project.id,
            "case_id": case_id
        }), 201
    except Exception as e:
        return jsonify({"error": f"Error en Bonita: {str(e)}"}), 500


@bonita_bp.post("/v1/login")
def bonita_login():
    """
    Realiza el login en Bonita y devuelve un mensaje de éxito o error.
    """
    # Recibe el JSON del body.
    data = request.get_json(silent=True) or {}
    
    # Realiza el login con Bonita.
    bonita = BonitaService()
    if bonita.bonita_login(data):
        return jsonify({"message": "Login en Bonita exitoso."}), 201
    else:
        return jsonify({"error": "No se pudo autenticar en Bonita"}), 500