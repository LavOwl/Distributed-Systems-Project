from src.web.handlers.helpers import get_authenticated_bonita_service
from src.web.handlers.authentication import require_bonita_auth
from flask import Blueprint, jsonify, request, g
from src.web.services import observation_service
from src.web.services import project_service
from werkzeug.exceptions import BadRequest
from pydantic import ValidationError
import json
project_bp = Blueprint("project", __name__)

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
          # Creación del proyecto.
        project = project_service.create_project_from_payload(data, user_id)
        #inicio el proceso en Bonita
        stages_required_contribution = project_service.stages_require_contribution(project.stages)
                
        # Seteo de la variable de número de etapas al proceso de Bonita.
        numero_etapas = project_service.contar_etapas_colaborativas(data)
        
        print(stages_required_contribution)
        print(type(stages_required_contribution))

        case_id = bonita.iniciar_proceso_con_datos(
            "proceso_de_ejecucion",
            {
                "stages": stages_required_contribution, "numero_etapas": numero_etapas
            }
        )
        project_service.link_to_bonita_case(project, case_id)
        bonita.completar_tarea(case_id)
        
        return jsonify({"stages": stages_required_contribution}), 200
    except ValidationError as e:
            return jsonify({"errors": e.errors()}), 400
    #     return jsonify({"message": "Proyecto creado correctamente."}), 201
    # 


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
    # Obtención de las cookies de la sesión actual.
    bonita = get_authenticated_bonita_service()

    # Inicia el proceso de control.
    case_id = bonita.iniciar_proceso("proceso_de_control")

    # Guarda el case_id asociado al proceso en una variable global separada.
    observation_service.set_current_case(case_id)

    # Completa la tarea actual del consejo directivo.
    bonita.completar_tarea(case_id)
    
    # Busca los proyectos y los retorna.
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
        # Obtención de las cookies de la sesión actual.
        bonita = get_authenticated_bonita_service()

        # Obtiene el case_id actual.
        case_id = observation_service.get_current_case()
        
        # Incrementa la variable de cantidad de observaciones en Bonita.
        contador_actual = bonita.obtener_variable_de_caso(case_id, "contador_observaciones")
        bonita.establecer_variable_al_caso(case_id, "contador_observaciones", contador_actual + 1, "java.lang.Integer")

        # Crea la observación, almacenando el case_id en ella.
        project_service.add_observation(case_id, project_id, data)
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {str(e)}"}), 500
    return jsonify({"message": f"Observación agregada correctamente al proyecto."}), 201


@project_bp.post("/v1/finalizar_revision")
@require_bonita_auth("consejo_directivo")
def finalizar_revision():
    """
    Finaliza la tarea de revisión del Consejo Directivo en Bonita.
    Solo completa la tarea activa y permite avanzar al siguiente paso.
    (1) No recibe nada.
    (2) Devuelve:
        1. 200 - message: revisión finalizada correctamente.
        2. 401 - error: sesión expirada o inválida.
        3. 403 - error: el usuario no tiene permisos para acceder.
        4. 500 - error: ocurrió un error inesperado.
    """
    try:
        # Obtención del servicio Bonita autenticado.
        bonita = get_authenticated_bonita_service()

        # Obtiene el case_id actual.
        case_id = observation_service.get_current_case()

        # Completa la tarea actual del consejo directivo.
        bonita.completar_tarea(case_id)

        return jsonify({"message": "Revisión finalizada correctamente."}), 200
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {str(e)}"}), 500


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
        user_id = g.bonita_user["user_id"]
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

    # Obtenemos el case_id de la observación.
    case_id = observation.case_id

    # Completamos la tarea en Bonita.
    bonita = get_authenticated_bonita_service()
    bonita.completar_tarea(case_id)

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


@project_bp.get("/v1/debug/case-variables/<case_id>")
@require_bonita_auth("ong_originante")
def get_case_variables(case_id):
    """
    Endpoint de debug: muestra las variables de un caso de Bonita.
    """
    try:
        bonita = get_authenticated_bonita_service()
        variables = bonita.obtener_variables_caso(case_id)
        
        return jsonify({
            "case_id": case_id,
            "variables": variables
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500