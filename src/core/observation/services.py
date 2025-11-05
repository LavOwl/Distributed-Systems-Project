from src.core.observation.model import Observation
from src.core.observation.model import Status
from src.core.database import db

def create_observation(project_id: int, name: str, description: str, status):
    """
    Crea una nueva observación asociada a un proyecto y la guarda en la base de datos.
    """
    new_observation = Observation(
        id_project=project_id,
        name=name,
        description=description,
        status=status
    )

    db.session.add(new_observation)
    db.session.commit()
    
    return new_observation


def mark_observation_as_resolved(observation_id: int):
    """
    Marca una observación como completa, si existe.
    """
    observation = Observation.query.get(observation_id)

    if not observation:
        return None

    observation.status = Status.RESOLVED
    db.session.commit()

    return observation