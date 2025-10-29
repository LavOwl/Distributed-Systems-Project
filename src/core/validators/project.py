from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum as PyEnum

from src.core.validators.stage import StageSchema as ProjectStageValidator


class ProjectValidator(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
   
    stages: Optional[List[ProjectStageValidator]] = []

    @validator('title')
    def validate_name_not_empty(cls, name_value):
        if not name_value or not name_value.strip():
            raise ValueError('El nombre no puede estar vacío')
        return name_value

    @validator('description')
    def validate_description_length(cls, description_value):
        if description_value and len(description_value) > 255:
            raise ValueError('La descripción no puede tener más de 255 caracteres')
        return description_value