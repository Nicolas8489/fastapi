# Semana 2 - main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# Inicializar la app
app = FastAPI(title="Semana 2 - API con Type Hints, Pydantic y Parámetros")

# ---------------------------
# Modelos de datos
# ---------------------------
class Product(BaseModel):
    name: str
    price: int  # en centavos para evitar decimales
    available: bool = True

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Successful operation"

class ProductListResponse(BaseModel):
    products: List[dict]
    total: int
    message: str = "List retrieved successfully"

# ---------------------------
# Almacenamiento temporal
# ---------------------------
products = []

# ---------------------------
# Endpoints básicos (Práctica 3)
# ---------------------------
@app.get("/")
def hello_world() -> dict:
    return {"message": "Semana 2 - API funcionando con FastAPI"}

# ---------------------------
# Endpoints con Pydantic (Práctica 4)
# ---------------------------
@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)

    return ProductResponse(**product_dict, message="Product created successfully")

@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(
        products=products,
        total=len(products)
    )

# ---------------------------
# Endpoints con parámetros (Práctica 5)
# ---------------------------
@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/categories/{category}/products/{product_id}")
def product_by_category(category: str, product_id: int) -> dict:
    return {
        "category": category,
        "product_id": product_id,
        "message": f"Searching product {product_id} in {category}"
    }

@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None,
    available: Optional[bool] = None
) -> dict:
    results = products.copy()

    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    if available is not None:
        results = [p for p in results if p["available"] == available]

    return {"results": results, "total": len(results)}
