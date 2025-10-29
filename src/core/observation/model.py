from src.core.database import db
from sqlalchemy import Enum
import enum

class Status(enum.Enum):
    """
    Enum para los estados de una observación.
    """
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"

class Observation(db.Model):
    """
    Modelo para representar la etapa de un proyecto.
    """
    __tablename__ = "observations"
    id = db.Column(db.Integer, primary_key=True)
    id_project = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(Enum(Status), nullable=False, default=Status.PENDING)