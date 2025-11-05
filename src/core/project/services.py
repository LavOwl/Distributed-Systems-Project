from src.core.stage.services import crear_stage
from src.core.project.model import Project
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from src.core.database import db

def create_project(name, description, stages) -> Project:
    """
    Creación de un proyecto y de sus stages asociados.
    """
    try:
        # Seteo de variables.
        project = Project(
            name=name,
            description=description,
         
        )
        
        # Almacenamiento del project en la base de datos.
        db.session.add(project)
        db.session.flush()

        # Creación de los stages asociados.
        for stage in stages:
            crear_stage(
                id_project=project.id,
                name=stage["name"],
                start_date=stage["start_date"],
                end_date=stage.get("end_date"),
                coverage_request=stage["coverage_request"],
                requires_contribution=stage["requires_contribution"]
            )

        # Commit en la base de datos para persistir las relaciones.
        db.session.commit()

        # Devolvemos el proyecto creado.
        return project
    except SQLAlchemyError as error:
        
        # Manejo del error en caso que la base de datos falle.
        db.session.rollback()
        raise Exception(f"Error al registrar el stage.")


def set_case_id(project: Project, case_id):
    """
    Setea el case_id de Bonita para un proyecto existente.
    """
    try:
        # Setea el case_id y lo persiste.
        project.case_id = case_id
        db.session.commit()
    except SQLAlchemyError as error:

        # Manejo del error en caso que la base de datos falle.
        db.session.rollback()
        raise Exception(f"No se pudo actualizar el case_id: {error}")


def get_projects_with_all_the_stages():
    """
    Devuelve todos los proyectos con todas sus etapas.
    """
    projects = Project.query.options(joinedload(Project.stages)).all()
    return projects