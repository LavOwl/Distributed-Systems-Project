from src.core.database import db
from sqlalchemy import Enum
import enum
from src.core.stage.model import Stage

class ProjectStatus(enum.Enum):
    """Enum para los estados de un proyecto."""
    PENDING = "Pendiente"
    IN_PROGRESS = "En progreso"
    COMPLETED = "Completado"


class Project(db.Model):
    """Modelo para representar un proyecto."""
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(Enum(ProjectStatus), default=ProjectStatus.PENDING, nullable=False)

    """Relación entre project y stage."""
    stages = db.relationship("Stage", back_populates="project")