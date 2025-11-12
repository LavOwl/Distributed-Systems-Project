from src.core.validators.stage import StageSchema as ProjectStageValidator
from pydantic import BaseModel, Field, validator
from typing import List

class ProjectValidator(BaseModel):
    """
    Esquema de validación de datos con Pydantic.
    """
    name: str = Field(..., description="Nombre del proyecto")
    description: str = Field(..., description="Descripción del proyecto")
    stages: List[ProjectStageValidator] = Field(..., description="Lista de etapas del proyecto")

    @validator("name")
    def validate_name_not_empty(cls, name_value):
        if not name_value or not name_value.strip():
            raise ValueError("El nombre no puede estar vacío")
        if len(name_value) > 100:
            raise ValueError("El nombre no puede tener más de 100 caracteres")
        return name_value

    @validator("description")
    def validate_description_length(cls, description_value):
        if not description_value or not description_value.strip():
            raise ValueError("La descripción no puede estar vacía")
        if len(description_value) > 255:
            raise ValueError("La descripción no puede tener más de 255 caracteres")
        return description_value

    @validator("stages")
    def validate_stages_not_empty(cls, stages_value):
        if not stages_value or len(stages_value) == 0:
            raise ValueError("El proyecto debe tener al menos una etapa")
        return stages_value