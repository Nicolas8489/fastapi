from fastapi import APIRouter
from ..cache.cache_decorators import cache_result

router = APIRouter(prefix="/real_", tags=["Real Estate"])

@router.get("/properties/frequent")
@cache_result()
async def get_frequent_properties():
    return [{"id": 1, "name": "Casa Central", "location": "Bogotá"}]

@router.get("/properties/{location}")
@cache_result()
async def get_properties_by_location(location: str):
    return [{"id": 2, "name": f"Casa en {location}", "price": 200000}]
