from src.core.database import db
from sqlalchemy import Enum
import enum

class CoverageRequest(enum.Enum):
    """
    Enum para los pedidos de cobertura de un proyecto.
    """
    DINERO = "DINERO"
    MATERIALES = "MATERIALES"
    MANO_DE_OBRA = "MANO_DE_OBRA"

class StatusStage(enum.Enum):
    """
    Enum para los estados de una etapa del proyecto.
    """
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"

class Stage(db.Model):
    """
    Modelo para representar la etapa de un proyecto.
    """
    __tablename__ = "stages"
    id = db.Column(db.Integer, primary_key=True)
    id_project = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)
    coverage_request = db.Column(Enum(CoverageRequest), nullable=False)
    status = db.Column(Enum(StatusStage), default=StatusStage.PENDING, nullable=False)
    
    
    def to_dict(self):
           return {
                "id": self.id,
                "id_project": self.id_project,
                "name": self.name,
                "description": self.description,
                "start_date": self.start_date.isoformat() if self.start_date else None,
                "end_date": self.end_date.isoformat() if self.end_date else None,
                "coverage_request": self.coverage_request.name if self.coverage_request else None,
                "status": self.status.name if self.status else None
            }