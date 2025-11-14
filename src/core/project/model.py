from src.core.database import db

class Project(db.Model):
    """
    Modelo para representar un proyecto.
    """
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    # Relación entre project y stage.
    stages = db.relationship("Stage", back_populates="project")

    # Relación entre project y observation.
    observations = db.relationship("Observation", back_populates="project")
    
    def to_dict(self):
        return {
            "id": self.id,
            "case_id": self.case_id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description
        }