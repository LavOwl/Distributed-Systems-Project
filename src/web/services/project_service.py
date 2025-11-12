from src.core.observation import services as core_observation_services
from src.core.validators.observation import ObservationValidator
from src.core.project import services as core_project_services
from src.core.validators.project import ProjectValidator
from werkzeug.exceptions import BadRequest

def create_project(payload, user_id, case_id):
    """
    Valida el payload y crea el proyecto con sus stages, y retorna el proyecto creado o lanza ValidationError.
    """
    project_in = ProjectValidator.model_validate(payload)
    name = project_in.name
    description = project_in.description or ""
    stages = [stage.model_dump() for stage in project_in.stages]
    return core_project_services.create_project(user_id, case_id, name, description, stages)


def link_to_bonita_case(project, case_id):
    """
    Vincula un proyecto con un case_id de Bonita.
    """
    core_project_services.link_to_bonita_case(project, case_id)


def get_projects_with_stages():
    """
    Devuelve todos los proyectos junto a todas sus etapas.
    """
    projects = core_project_services.get_projects_with_stages()
    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "name": p.name,
            "description": p.description,
            "stages": [s.to_dict() for s in p.stages]
        }
        for p in projects
    ]


def add_observation(case_id: int, project_id: int, data: dict):
    """
    Valida los datos y crea una observación asociada a un proyecto.
    """
    try:
        validated = ObservationValidator(**data)
    except Exception as e:
        raise BadRequest(str(e))
    observation = core_observation_services.add_observation(
        case_id=case_id,
        project_id=project_id,
        name=validated.name,
        description=validated.description,
        status=validated.status
    )
    return observation


def get_observations_by_user(user_id: int):
    """
    Obtiene todas las observaciones asociadas a los proyectos del usuario.
    """
    observations = core_observation_services.get_observations_by_user(user_id)
    return [obs.to_dict() for obs in observations]


def upload_corrected_observation(observation_id: int):
    """
    Marca una observación como completa.
    """
    return core_observation_services.upload_corrected_observation(observation_id)


def contar_etapas_colaborativas(data):
    """
    A partir del JSON recibido al crear un proyecto, cuenta cuántas etapas requieren colaboración.
    """
    etapas = data.get("stages", [])
    return sum(1 for etapa in etapas if etapa.get("requires_contribution"))