from src.core.project.services import create_project, set_case_id
from src.core.validators.project import ProjectValidator

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