from src.core.database import db
from src.core.stage.model import Stage, CoverageRequest, StatusStage
from sqlalchemy.exc import SQLAlchemyError

def crear_stage(project_id, coverage_request, requires_contribution, name, start_date, end_date=None):
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
            requires_contribution=requires_contribution,
            project_id=project_id
        )

        # Almacenamiento del stage en la base de datos.
        db.session.add(stage)
        db.session.commit()
    except SQLAlchemyError as error:
        
        # Manejo del error en caso que la base de datos falle.
        db.session.rollback()
        raise Exception(f"Error al registrar el stage.")
    

def get_stages_by_project_id(project_id: int):
    """
    Obtiene las etapas asociadas a un proyecto.
    """
    stages = Stage.query.filter_by(id_project=project_id, status=StatusStage.PENDING, requires_contribution = True).all()
    return stages

def get_all_stages_by_project():
    """
    Obtiene todas las etapas de todos los proyectos.
    """
    stages = Stage.query.filter_by(status=StatusStage.PENDING, requires_contribution = True).all()
    return stages