from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from .app import auth, crud
from . import models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Completa - Bootcamp FastAPI")
security = HTTPBearer()

# Endpoints de Semana 1
@app.get("/")
def read_root() -> dict:
    return {"message": "🚀 Bienvenido a la API Completa de FastAPI"}

@app.get("/ejercicio")
def ejercicio() -> dict:
    return {"result": "✅ Ejercicio de la Semana 1"}

@app.get("/info/setup")
def info_setup() -> dict:
    return {
        "status": "ok",
        "message": "🚀 Setup FastAPI funcionando correctamente",
        "docs": "http://localhost:8000/docs",
        "server": "http://localhost:8000"
    }

# Endpoints de Semana 2 (simplificados con base de datos)
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.crear_producto(db, product)

@app.get("/products", response_model=List[schemas.ProductResponse])
def get_products(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    return crud.obtener_productos(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.obtener_producto(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.get("/search", response_model=List[schemas.ProductResponse])
def search_product(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return crud.buscar_productos(db, q)

# Endpoints de Semana 3 y 4 (CRUD completo)
@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, updates: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = crud.actualizar_producto(db, product_id, updates)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.eliminar_producto(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": f"Producto {product_id} eliminado"}

# Endpoints de Semana 4 (Categorías)
@app.post("/categorias/", response_model=schemas.Categoria)
def create_category(category: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.crear_categoria(db, category)

@app.get("/categorias/", response_model=List[schemas.Categoria])
def list_categories(db: Session = Depends(get_db)):
    return crud.obtener_categorias(db)

@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaConProductos)
def get_category(categoria_id: int, db: Session = Depends(get_db)):
    category = crud.obtener_categoria_con_productos(db, categoria_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

# Endpoints de Semana 4 (Estadísticas y Health)
@app.get("/productos/stats/resumen")
def estadisticas_productos(db: Session = Depends(get_db)):
    total = crud.contar_productos(db)
    productos = crud.obtener_productos(db, limit=total)
    if not productos:
        return {"total": 0, "precio_promedio": 0, "precio_max": 0, "precio_min": 0}
    precios = [p.precio for p in productos]
    return {
        "total": total,
        "precio_promedio": sum(precios) / len(precios),
        "precio_max": max(precios),
        "precio_min": min(precios)
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}

# Endpoints de Semana 5 (Autenticación)
@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.Token)
def login_user(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@app.get("/protected")
def protected_endpoint(current_user: models.User = Depends(auth.get_current_user)):
    return {"message": f"Hola {current_user.username}, tienes acceso!", "user_id": current_user.id, "status": "authenticated"}

@app.post("/create-admin", response_model=schemas.UserResponse)
def create_first_admin(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(models.User).filter(models.User.role == "admin").first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Ya existe un administrador")
    if auth.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username ya registrado")
    admin_user = auth.create_admin_user(db, user_data.username, user_data.email, user_data.password)
    return schemas.UserResponse(id=admin_user.id, username=admin_user.username, email=admin_user.email, is_active=admin_user.is_active, role=admin_user.role)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor...")
    print("👉 Acceder a: http://localhost:8000")
    print("📑 Documentación: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)