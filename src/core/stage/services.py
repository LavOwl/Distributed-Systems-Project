from src.core.database import db
from src.core.stage.model import Stage, CoverageRequest
from sqlalchemy.exc import SQLAlchemyError

def crear_stage(project_id, coverage_request, name, start_date, end_date=None):
    """
    Creación de un stage asociado a un proyecto.
    """
    try:
        # Seteo de variables.
        stage = Stage(
            name=name,
            start_date=start_date,
            end_date=end_date,
            coverage_request=CoverageRequest[coverage_request],
            project_id=project_id
        )

        # Almacenamiento del stage en la base de datos.
        db.session.add(stage)
        db.session.commit()
    except SQLAlchemyError as error:
        
        # Manejo del error en caso que la base de datos falle.
        db.session.rollback()
        raise Exception(f"Error al registrar el stage.")