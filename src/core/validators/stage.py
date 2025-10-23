from src.core.database import db
from sqlalchemy import Enum
import enum
from src.core.stage.model import CoverageRequest
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


# Esquema de validación de datos con Pydantic
class StageSchema(BaseModel):
    name: str = Field(..., max_length=100)
    start_date: datetime
    end_date: Optional[datetime] = None
    coverage_request: CoverageRequest
    requires_contributor: bool = False

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if v and 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v
    
    class Config:
        use_enum_values = True