from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mi API Semana 2")

# Modelo Pydantic
class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# Base de datos simulada
products_db: list[Product] = []

@app.get("/")
def home() -> dict:
    return {"message": "Bienvenido a la API de la Semana 2 🚀"}

@app.post("/products")
def create_product(product: Product) -> dict:
    products_db.append(product)
    return {"message": "Producto creado", "product": product.dict()}

@app.get("/products")
def get_products() -> dict:
    return {"products": [p.dict() for p in products_db]}

@app.get("/products/{id}")
def get_product(id: int) -> dict:
    for product in products_db:
        if product.id == id:
            return {"product": product.dict()}
    return {"error": "Producto no encontrado"}

@app.get("/search")
def search_product(name: str) -> dict:
    results = [p.dict() for p in products_db if name.lower() in p.name.lower()]
    return {"results": results}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor de la Semana 2...")
    print("👉 Acceder a: http://localhost:8000")
    print("📑 Documentación: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
