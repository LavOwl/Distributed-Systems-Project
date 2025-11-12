from src.core.observation.model import Observation
from src.core.observation.model import Status
from src.core.project.model import Project
from src.core.database import db

def add_observation(case_id: int, project_id: int, name: str, description: str, status):
    """
    Crea una nueva observación asociada a un proyecto y la guarda en la base de datos.
    """
    new_observation = Observation(
        case_id=case_id,
        id_project=project_id,
        name=name,
        description=description,
        status=status
    )
    db.session.add(new_observation)
    db.session.commit()
    return new_observation


def get_observations_by_user(user_id: int):
    """
    Obtiene todas las observaciones con estado PENDING
    asociadas a los proyectos creados por un usuario.
    """
    observations = (
        Observation.query
        .join(Project)
        .filter(Project.user_id == user_id)
        .filter(Observation.status == Status.PENDING)
        .all()
    )
    return observations


def upload_corrected_observation(observation_id: int):
    """
    Marca una observación como completa, si existe.
    """
    observation = Observation.query.get(observation_id)
    if not observation:
        return None
    observation.status = Status.RESOLVED
    db.session.commit()
    return observation