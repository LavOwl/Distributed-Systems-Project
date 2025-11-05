from pydantic import BaseModel, Field, validator
from src.core.observation.model import Status
from typing import Optional

class ObservationValidator(BaseModel):
    """
    Esquema de validación de datos para la creación o actualización de observaciones.
    """
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    status: Optional[Status] = Field(default=Status.PENDING)

    @validator("name")
    def validate_name_not_empty(cls, name_value: str):
        if not name_value or not name_value.strip():
            raise ValueError("El nombre de la observación no puede estar vacío")
        return name_value

    @validator("description")
    def validate_description_length(cls, description_value: Optional[str]):
        if description_value and len(description_value) > 255:
            raise ValueError("La descripción no puede tener más de 255 caracteres")
        return description_value