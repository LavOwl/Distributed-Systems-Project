from src.core.stage.services import crear_stage
from src.core.project.model import Project
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from src.core.database import db

def create_project(user_id, name, description, stages) -> Project:
    """
    Creación de un proyecto y de sus stages asociados.
    """
    try:
        # Seteo de variables.
        project = Project(
            user_id=user_id,
            name=name,
            description=description
        )
        
        # Almacenamiento del proyecto en la base de datos.
        db.session.add(project)
        db.session.flush()

        # Creación de los stages asociados.
        for stage in stages:
            crear_stage(
                id_project=project.id,
                name=stage["name"],
                description=stage["description"],
                start_date=stage["start_date"],
                end_date=stage.get("end_date"),
                coverage_request=stage["coverage_request"],
                requires_contribution=stage["requires_contribution"]
            )

        db.session.commit()
        return project
    except SQLAlchemyError as error:
        db.session.rollback()
        raise Exception(f"Error al registrar el proyecto.")


def link_to_bonita_case(project: Project, case_id):
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


def get_projects_with_stages():
    """
    Devuelve todos los proyectos con todas sus etapas.
    """
    projects = Project.query.options(joinedload(Project.stages)).all()
    return projects

def get_project_by_case_id(case_id: int):
    """
    Obtiene un proyecto a partir de su case_id de Bonita.
    """
    project = Project.query.filter_by(case_id=case_id).first()
    return project