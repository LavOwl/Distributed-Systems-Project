from src.web.handlers.authentication import require_bonita_auth
from src.web.services.bonita_service import BonitaService
from flask import Blueprint, jsonify, request, g
from src.web.services import project_service
from werkzeug.exceptions import BadRequest
from pydantic import ValidationError

project_bp = Blueprint("project", __name__)

def get_authenticated_bonita_service():
        """
        Helper: recupera cookies de autenticación y devuelve un BonitaService configurado.
        Lanza ValueError si no hay cookies válidas.
        """
        csrf_token = request.cookies.get("X-Bonita-API-Token")
        jsessionid = request.cookies.get("JSESSIONID") 
        if not csrf_token or not jsessionid:
            raise ValueError("Sesión de Bonita no válida o expirada")
        bonita = BonitaService()
        bonita.csrf_token = csrf_token
        bonita.session.cookies.set("JSESSIONID", jsessionid)
        bonita.session.cookies.set("X-Bonita-API-Token", csrf_token)        
        return bonita


@project_bp.post("/v1/create_project")
@require_bonita_auth("ong_originante")
def create_project():
    """
    Crea un proyecto con los datos recibidos.
    (1) Recibe (JSON en el BODY):
        1. name: string.
        2. description: string.
    (2) Devuelve:
        1. 201 - message: proyecto creado correctamente.
        2. 401 - error: sesión expirada o inválida.
        3. 403 - error: el usuario no tiene permisos para acceder.
    """
    try:
        # Obtener los datos del body.
        data = request.get_json()

        # Obtención del user_id de la sesión actual.
        user_id = g.bonita_user["user_id"]

        # Obtención de las cookies de la sesión actual.
        bonita = get_authenticated_bonita_service()

        # Iniciación del proceso en Bonita.
        case_id = bonita.iniciar_proceso("proceso_de_ejecucion")

        # Creación del proyecto.
        project_service.create_project(data, user_id, case_id)
        bonita.completar_tarea(case_id)
        
        return jsonify({"message": "Proyecto creado correctamente."}), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400


@project_bp.get("/v1/get_projects_with_stages")
@require_bonita_auth("consejo_directivo")
def get_projects_with_stages():
    """
    Devuelve todos los proyectos con todas sus etapas.
    (1) No recibe nada.
    (2) Devuelve:
        1. 200 - lista de proyectos con sus etapas.
        2. 401 - error: sesión expirada o inválida.
        3. 403 - error: el usuario no tiene permisos para acceder.
    """
    result = project_service.get_projects_with_stages()
    return jsonify(result)


@project_bp.post("/v1/add_observation/<int:project_id>")
@require_bonita_auth("consejo_directivo")
def add_observation(project_id: int):
    """
    Agrega una observación a un proyecto a partir de su ID de proyecto.
    (1) Recibe (parámetro en la ruta):
        1. project_id: int.
    (2) Recibe (JSON en el BODY):
        1. name: string.
        2. description: string.
    (3) Devuelve:
        1. 201 - message: observación agregada correctamente al proyecto
        2. 400 - error: el nombre de la observación no puede estar vacío.
        3. 400 - error: la descripción no puede tener más de 255 caracteres.
        4. 401 - error: sesión expirada o inválida.
        5. 403 - error: el usuario no tiene permisos para acceder.
        6. 500 - error: ocurrió un error inesperado.
    """
    data = request.get_json()
    try:
        project_service.add_observation(project_id, data)
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {str(e)}"}), 500
    return jsonify({"message": f"Observación agregada correctamente al proyecto."}), 201


@project_bp.get("/v1/get_observations_by_user")
@require_bonita_auth("ong_originante")
def get_observations_by_user():
    """
    Lista todas las observaciones asociadas a los proyectos del usuario autenticado.
    (1) No recibe nada.
    (2) Devuelve:
        1. 200 - lista de observaciones del usuario.
        2. 401 - error: sesión expirada o inválida.
        3. 403 - error: el usuario no tiene permisos para acceder.
        4. 404 - message: no se encontraron observaciones.
        5. 500 - error: ocurrió un error inesperado.
    """
    try:
        user_id = g.bonita_user.user_id
        observations = project_service.get_observations_by_user(user_id)
        if not observations:
            return jsonify({"message": "No se encontraron observaciones asociadas a tus proyectos."}), 404
        return jsonify(observations), 200
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {str(e)}"}), 500


@project_bp.patch("/v1/upload_corrected_observation/<int:observation_id>")
@require_bonita_auth("ong_originante")
def upload_corrected_observation(observation_id: int):
    """
    Marcar una observación como completada a partir de su ID.
    (1) Recibe (parámetro en la ruta):
        1. observation_id: int.
    (2) Devuelve:
        1. 200 - message: la observación ha sido marcada como completada.
        2. 404 - message: no se encontró la observación.
        3. 401 - error: sesión expirada o inválida.
        4. 403 - error: el usuario no tiene permisos para acceder.
    """
    observation = project_service.upload_corrected_observation(observation_id)
    if not observation:
        return jsonify({"message": f"No se encontró la observación."}), 404
    return jsonify({"message": f"La observación ha sido marcada como completada."}), 200


@project_bp.get("/v1/siguiente")
@require_bonita_auth("ong_originante")
def avanzar():
    """
    Avanza la tarea actual en Bonita para el proyecto asociado al usuario.
    (1) No recibe nada.
    (2) Devuelve:
        1. 200 - message: tarea avanzada correctamente.
        2. 401 - error: sesión expirada o inválida.
        3. 403 - error: el usuario no tiene permisos para acceder.
    """
    # Obtención de las cookies de la sesión actual.
    bonita = get_authenticated_bonita_service()
    case_id = request.get_json().get("case_id")

    # Avance de la tarea en Bonita.
    bonita.completar_tarea(case_id)

    return jsonify({"message": "Tarea avanzada correctamente."}), 200