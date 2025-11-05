from src.web.services.bonita_service import BonitaService
from flask import Blueprint, request, jsonify
from src.web.services import project_service
from pydantic import ValidationError
import os

bonita_bp = Blueprint("bonita", __name__)
BONITA_BASE_URL = os.environ.get("BONITA_BASE_URL")

@bonita_bp.post("/v1/login")
def bonita_login():
    """
    Realiza el login en Bonita y devuelve un mensaje de éxito o error.
    (1) Recibe (JSON en el BODY):
        1. username: string.
        2. password: string.
    (2) Devuelve:
        1. 401 - No se pudo autenticar en Bonita.
        2. 200 - Login exitoso.
    """
    # Recibe el JSON del body, y hace el login con Bonita.
    data = request.get_json(silent=True) or {}
    bonita = BonitaService()
    session = bonita.bonita_login(data)

    # Verifica si se puede autenticar correctamente.
    if not session:
            return jsonify({"error": "No se pudo autenticar en Bonita"}), 401
    
    # Obtiene las cookies desde la sesión.
    jsessionid = session.cookies.get("JSESSIONID")
    token = session.cookies.get("X-Bonita-API-Token")

    # Devolverlas al cliente (por header o cookie HTTP)
    response = jsonify({"message": "Login exitoso"})
    response.set_cookie("JSESSIONID", jsessionid)
    response.set_cookie("X-Bonita-API-Token", token)
    return response, 200


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