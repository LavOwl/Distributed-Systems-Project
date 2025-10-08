from src.core.database import db
from src.core.project.model import Project, ProjectStatus
from src.core.stage.services import crear_stage
from sqlalchemy.exc import SQLAlchemyError

def crear_project(name, description, stages):
    """
    Creación de un proyecto y de sus stages asociados.
    """
    try:
        # Seteo de variables.
        project = Project(
            name=name,
            description=description,
            status=ProjectStatus.PENDIENTE
        )
        
        # Almacenamiento del project en la base de datos.
        db.session.add(project)
        db.session.flush()

        # Creación de los stages asociados.
        for stage in stages:
            crear_stage(
                project_id=project.id,
                name=stage["name"],
                start_date=stage["start_date"],
                end_date=stage.get("end_date"),
                coverage_request=stage["coverage_request"]
            )

        # Commit en la base de datos para persistir las relaciones.
        db.session.commit()
    except SQLAlchemyError as error:
        
        # Manejo del error en caso que la base de datos falle.
        db.session.rollback()
        raise Exception(f"Error al registrar el stage.")