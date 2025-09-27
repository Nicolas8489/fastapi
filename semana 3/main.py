from fastapi import FastAPI, HTTPException
from typing import List
from models.product_models import Product, ProductCreate, ProductUpdate
from data.products_data import products_db, get_product_by_id

app = FastAPI(title="Semana 3 - CRUD Productos")

# Listar todos los productos
@app.get("/products", response_model=List[Product])
def list_products():
    return products_db

# Obtener producto por ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

# Crear producto
@app.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    new_id = max([p.id for p in products_db], default=0) + 1
    new_product = Product(id=new_id, **product.dict())
    products_db.append(new_product)
    return new_product

# Actualizar producto
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, updates: ProductUpdate):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    return product

# Eliminar producto
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    products_db.remove(product)
    return {"message": f"Producto {product_id} eliminado exitosamente"}
