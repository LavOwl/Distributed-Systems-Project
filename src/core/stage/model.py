from src.core.database import db
from sqlalchemy import Enum
import enum
from src.core.project.model import Project

class CoverageRequest(enum.Enum):
    """
    Enum para los pedidos de cobertura de un proyecto.
    """
    DINERO = "Dinero"
    MATERIALES = "Materiales"
    MANO_DE_OBRA = "Mano de obra"


class Stage(db.Model):
    """
    Modelo para representar la etapa de un proyecto.
    """
    __tablename__ = "stage"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    coverage_request = db.Column(Enum(CoverageRequest), nullable=False)

    # Clave foránea para acceder al proyecto.
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    # Relación entre project y stage.
    project = db.relationship("Project", back_populates="stages")