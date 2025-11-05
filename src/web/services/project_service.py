from src.core.project.services import create_project, set_case_id, get_projects_with_all_the_stages
from src.core.validators.observation import ObservationValidator
from src.core.observation.services import create_observation 
from src.core.validators.project import ProjectValidator
from werkzeug.exceptions import BadRequest

def create_project_from_payload(payload):
    """
    Valida el payload y crea el proyecto con sus stages, y retorna el proyecto creado o lanza ValidationError.
    """
    # Validación de los datos.
    project_in = ProjectValidator.model_validate(payload)

    # Extracción de los datos.
    name = project_in.title
    description = project_in.description or ""
    stages = [stage.model_dump() for stage in project_in.stages]

    # Creación del proyecto.
    return create_project(name, description, stages)


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

    # Creación de la observación en la base de datos.
    observation = create_observation(
        project_id=project_id,
        name=validated.name,
        description=validated.description,
        status=validated.status
    )

    return observation