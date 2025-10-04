# app/models/schemas.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

class JoyaStatusEnum(str, Enum):
    ACTIVO = "activo"
    AGOTADO = "agotado"
    PENDIENTE = "pendiente"

class JoyaBase(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"sku": "AN01", "nombre": "Anillo Gold", "precio": 150.50}}
    )
    sku: str = Field(..., description="Código SKU único", max_length=8)
    nombre: str = Field(..., description="Nombre de la joya", max_length=100)
    precio: float = Field(..., description="Precio en USD", ge=0)
    stock: int = Field(..., description="Unidades en inventario", ge=0)

class JoyaCreate(JoyaBase):
    pass

class JoyaUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"precio": 200.00, "stock": 5}}
    )
    precio: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)

class JoyaResponse(JoyaBase):
    model_config = ConfigDict(
        json_schema_extra={"example": {"id": 1, "sku": "AN01", "precio": 150.50, "fecha_creacion": "2025-10-03T14:00:00"}}
    )
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    status: JoyaStatusEnum
