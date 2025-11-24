from src.core.stage import services
import os
import requests

def get_stages_project(project_id: int):
    """
    Obtiene las etapas asociadas a un proyecto.
    """
    stages = services.get_stages_by_project_id(project_id)
    return [stage.to_dict() for stage in stages]


def get_all_stages_by_project():
    """
    Obtiene todas las etapas pendientes de todos los proyectos.
    """
    stages = services.get_all_stages_by_project()
    return [stage.to_dict() for stage in stages]


def cover_stage(user_id, stage_id: int):
    """
    Cubre una etapa específica según su ID.
    """
    stage = services.get_pending_stage_by_id(stage_id)
    if not stage:
        return None
    return services.cover_stage(user_id, stage)


def get_case_id_by_stage(stage):
    """
    Obtiene el case_id del proyecto al que pertenece una etapa.
    """
    if not stage or not stage.project:
        return None
    return stage.project.case_id


def get_in_progress_stages_for_user(user_id: int):
    """
    Obtiene las etapas en progreso del usuario actual.
    """
    stages = services.get_in_progress_stages_by_user(user_id)
    return [stage.to_dict() for stage in stages]


def finish_stage(stage_id: int):
    """
    Finaliza una etapa específica según su ID (de IN_PROGRESS a FINISHED).
    """
    stage = services.get_in_progress_stage_by_id(stage_id)
    if not stage:
        return None
    return services.finish_stage(stage)


def project_has_started(stage_id: int) -> bool:
    return services.project_has_started(stage_id)


def get_token_cloud():
    """
    Obtiene el token de autenticación para la nube.
    """
    response = requests.post(
        f"{os.getenv('CLOUD_URL')}/login/v1/authenticate",
        json={
            "email": "ong_colaborativa@projectplanning.org",
            "password": "ong_colaborativa"
        }
    )
    return response.json().get("access_token")


def get_all_stages_cloud():
    """
    Obtiene todas las etapas pendientes de todos los proyectos desde la nube.
    """
    # Construir URL y headers (token opcional desde variables de entorno).
    url = f"{os.getenv('CLOUD_URL')}/stages/v1/get_all_available_stages"
    token = get_token_cloud()
    csrf_token = os.getenv('CLOUD_CSRF_TOKEN') or os.getenv('CLOUD_API_TOKEN')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Iniciar el proceso y realizar la request.
    session = requests.Session()
    response = session.get(url, headers=headers, json={})
    response.raise_for_status()

    # Normalizar respuesta a lista de dicts.
    data = response.json()
    if isinstance(data, dict) and 'stages' in data:
        stages = data['stages']
    elif isinstance(data, list):
        stages = data
    else:
        stages = [data] if data is not None else []
    return stages


def get_in_progress_stages_for_user_cloud(user_id: int):
    """
    Obtiene las etapas en progreso del usuario actual.
    """
    url = f"{os.getenv('CLOUD_URL')}/stages/v1/get_in_progress_stages"
    token = get_token_cloud()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers, json={"user_id": user_id})

    # Si hubo error en la nube, levantar la excepción.
    if response.status_code != 200:
        raise Exception(f"Error en API Nube: {response.status_code} - {response.text}")
    return response.json()


def cover_stage_cloud(user_id, stage_id: int):
    """
    Cubre una etapa específica según su ID en la nube.
    """
    url = f"{os.getenv('CLOUD_URL')}/stages/v1/cover_stage/{stage_id}"
    token = get_token_cloud()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.patch(url, headers=headers, json={"user_id": user_id})
    
    # Si hubo error en la nube, levantar la excepción.
    if response.status_code != 200:
        raise Exception(f"Error en API Nube: {response.status_code} - {response.text}")
    return response.json()


def finish_stage_cloud(stage_id: int):
    """
    Finaliza una etapa específica según su ID (de IN_PROGRESS a FINISHED) en la nube.
    """
    url = f"{os.getenv('CLOUD_URL')}/stages/v1/finish_stage/{stage_id}"
    token = get_token_cloud()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.patch(url, headers=headers, json={})
    
    # Si hubo error en la nube, levantar la excepción.
    if response.status_code != 200:
        raise Exception(f"Error en API Nube: {response.status_code} - {response.text}")
    return response.json()