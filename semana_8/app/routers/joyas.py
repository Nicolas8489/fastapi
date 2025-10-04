# app/routers/joyas.py
from fastapi import APIRouter, HTTPException
from ..models.schemas import JoyaCreate, JoyaUpdate, JoyaResponse
from ..docs.descriptions import TAGS_METADATA, ENDPOINT_DESCRIPTIONS, RESPONSE_DESCRIPTIONS
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["joyas"])

joyas_db = []
contador_id = 1

@router.post("/joyas", response_model=JoyaResponse, description=ENDPOINT_DESCRIPTIONS["crear_joya"])
async def crear_joya(joya: JoyaCreate):
    if any(j["sku"] == joya.sku for j in joyas_db):
        raise HTTPException(status_code=400, detail="SKU duplicado")
    new_joya = {"id": contador_id, **joya.model_dump(), "fecha_creacion": datetime.now(), "fecha_actualizacion": datetime.now(), "status": "activo"}
    joyas_db.append(new_joya)
    contador_id += 1
    return JoyaResponse(**new_joya)

@router.get("/joyas/{sku}", response_model=JoyaResponse, description=ENDPOINT_DESCRIPTIONS["obtener_joya"])
async def obtener_joya(sku: str):
    joya = next((j for j in joyas_db if j["sku"] == sku), None)
    if not joya:
        raise HTTPException(status_code=404, detail="Joya no encontrada")
    return JoyaResponse(**joya)
