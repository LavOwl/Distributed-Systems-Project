from src.core.project.services import create_project, set_case_id, get_projects_with_all_the_stages
from src.core.observation.services import create_observation, mark_observation_as_resolved
from src.core.validators.observation import ObservationValidator
from src.core.validators.project import ProjectValidator
from werkzeug.exceptions import BadRequest

def create_project_from_payload(payload, user_id):
    """
    Valida el payload y crea el proyecto con sus stages, y retorna el proyecto creado o lanza ValidationError.
    """
    project_in = ProjectValidator.model_validate(payload)

    name = project_in.name
    description = project_in.description or ""
    stages = [stage.model_dump() for stage in project_in.stages]

    return create_project(user_id, name, description, stages)


def link_to_bonita_case(project, case_id):
    """
    Vincula un proyecto con un case_id de Bonita.
    """
    set_case_id(project, case_id)


def list_projects_with_stages():
    """
    Devuelve todos los proyectos junto a todas sus etapas.
    """
    projects = get_projects_with_all_the_stages()
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


def add_observation(project_id: int, data: dict):
    """
    Valida los datos y crea una observación asociada a un proyecto.
    """
    try:
        validated = ObservationValidator(**data)
    except Exception as e:
        raise BadRequest(str(e))

    observation = create_observation(
        project_id=project_id,
        name=validated.name,
        description=validated.description,
        status=validated.status
    )

    return observation


def upload_corrected_observation(observation_id: int):
    """
    Marca una observación como completa.
    """
    return mark_observation_as_resolved(observation_id)