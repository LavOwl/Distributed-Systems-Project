from src.core.stage.model import Stage, CoverageRequest, StatusStage
from sqlalchemy.exc import SQLAlchemyError
from src.core.database import db

def crear_stage(id_project, coverage_request, requires_contribution, name, description, start_date, end_date=None):
    """
    Creación de un stage asociado a un proyecto.
    """
    try:
        # Seteo de variables.
        stage = Stage(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            coverage_request=CoverageRequest[coverage_request],
            requires_contribution=requires_contribution,
            id_project=id_project
        )

        # Almacenamiento del stage en la base de datos.
        db.session.add(stage)
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise Exception(f"Error al registrar el stage.")
    

def get_stages_by_project_id(project_id: int):
    """
    Obtiene las etapas pendientes asociadas a un proyecto.
    """
    stages = Stage.query.filter_by(id_project=project_id, status=StatusStage.PENDING, requires_contribution = True).all()
    return stages


def get_all_stages_by_project():
    """
    Obtiene todas las etapas pendientes de todos los proyectos.
    """
    stages = Stage.query.filter_by(status=StatusStage.PENDING, requires_contribution = True).all()
    return stages


def get_pending_stage_by_id(stage_id: int):
    """
    retorna una etapa por su ID, solo si está pendiente.
    """
    stage = Stage.query.filter_by(id=stage_id, status=StatusStage.PENDING).first()
    return stage


def cover_stage(stage: Stage):
    """
    Cubre una etapa específica según su ID.
    """
    try:
        stage.status = StatusStage.IN_PROGRESS
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise Exception(f"Error al registrar el stage.")
    return stage


def get_in_progress_stage_by_id(stage_id: int):
    """
    Retorna una etapa por su ID, solo si está en progreso.
    """
    stage = Stage.query.filter_by(id=stage_id, status=StatusStage.IN_PROGRESS).first()
    return stage


def finish_stage(stage: Stage):
    """
    Marca una etapa como finalizada (de IN_PROGRESS a FINISHED).
    """
    try:
        stage.status = StatusStage.FINISHED
        db.session.commit()
    except SQLAlchemyError as error:
        db.session.rollback()
        raise Exception("Error al finalizar la etapa.")
    return stage