from src.core.database import db
from sqlalchemy import Enum
import enum

# class ProjectStatus(enum.Enum):
#     """
#     Enum para los estados de un proyecto.
#     """
#     PENDIENTE = "Pendiente"
#     EN_PROGRESO = "En progreso"
#     COMPLETADO = "Completado"


class Project(db.Model):
    """
    Modelo para representar un proyecto.
    """
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    #status = db.Column(db.Enum(ProjectStatus), default=ProjectStatus.PENDIENTE, nullable=False)

    # Relación entre project y stage.
    stages = db.relationship("Stage", back_populates="project")