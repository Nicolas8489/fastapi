from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine
from .auth import get_current_user, create_access_token
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Nutrición - Bootcamp FICHA 3147246")

# Configurar CORS (opcional, permite acceso desde un frontend si lo necesitas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (ajústalos en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar OAuth2 para autenticación (usa el endpoint /auth/login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint básico de bienvenida (semana 1)
@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido a la API de Nutrición - FICHA 3147246"}

@app.get("/info/setup")
def info_configuracion():
    return {"estado": "API configurada correctamente", "versión": "1.0.0"}

# Crear un router para los endpoints de planes nutricionales
router = FastAPI()

# Endpoints para planes (nutriplans) con autenticación y CRUD

@router.post("/nutriplans/", response_model=schemas.Plan)
def crear_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # Verifica que el usuario sea nutricionista
    if current_user["role"] != "nutricionista":
        raise HTTPException(status_code=403, detail="Solo los nutricionistas pueden crear planes")
    return crud.crear_plan(db=db, plan=plan, usuario_id=current_user["id"])

@router.get("/nutriplans/", response_model=List[schemas.Plan])
def leer_planes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    planes = crud.get_plans(db, skip=skip, limit=limit)
    return planes

@router.get("/nutriplans/{plan_id}", response_model=schemas.Plan)
def leer_plan(plan_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_plan = crud.get_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return db_plan

@router.put("/nutriplans/{plan_id}", response_model=schemas.Plan)
def actualizar_plan(plan_id: int, plan: schemas.PlanCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_plan = crud.get_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    if current_user["role"] != "nutricionista":
        raise HTTPException(status_code=403, detail="Solo los nutricionistas pueden actualizar planes")
    return crud.update_plan(db=db, plan_id=plan_id, plan=plan)

@router.delete("/nutriplans/{plan_id}")
def eliminar_plan(plan_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_plan = crud.get_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    if current_user["role"] != "nutricionista":
        raise HTTPException(status_code=403, detail="Solo los nutricionistas pueden eliminar planes")
    crud.delete_plan(db=db, plan_id=plan_id)
    return {"mensaje": "Plan eliminado exitosamente"}

# Incluir el router en la aplicación principal
app.include_router(router, prefix="/nutriplans", tags=["planes"], dependencies=[Depends(get_current_user)])

# Endpoints de autenticación (semana 5)
@app.post("/auth/register", response_model=schemas.UserResponse)
def registrar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    return crud.create_user(db=db, user=user)

@app.post("/auth/login")
def login_usuario(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if not db_user or not crud.verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    access_token = create_access_token(data={"sub": db_user.username, "id": db_user.id, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}