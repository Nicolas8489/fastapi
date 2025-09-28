from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from . import auth, models
from .database import SessionLocal, engine
from .schemas import UserCreate, UserLogin, Token, UserResponse, UserRoleUpdate, PostCreate, PostResponse
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API con Autenticación Básica")
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = auth.hash_password(user.password)
    db_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """Login y obtener token"""
    user = auth.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    """Obtener perfil del usuario autenticado"""
    return current_user

@app.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(auth.get_current_user)):
    """Endpoint protegido de ejemplo"""
    return current_user

@app.get("/")
def read_root():
    """Endpoint público sin autenticación"""
    return {"message": "API pública sin autenticación"}

@app.get("/protected")
def protected_endpoint(current_user: User = Depends(auth.get_current_user)):
    """Endpoint protegido básico"""
    return {"message": f"Hola {current_user.username}, tienes acceso!", "user_id": current_user.id, "status": "authenticated"}

@app.get("/public")
def public_endpoint():
    """Endpoint público sin protección"""
    return {"message": "Este endpoint es público", "status": "no authentication required"}

posts = []
@app.post("/posts", response_model=PostResponse)
def create_post(post_data: PostCreate, current_user: User = Depends(auth.get_current_user)):
    """Crear nuevo post (requiere autenticación)"""
    new_post = {
        "id": len(posts) + 1,
        "title": post_data.title,
        "content": post_data.content,
        "author": current_user.username
    }
    posts.append(new_post)
    return PostResponse(**new_post)

@app.get("/posts", response_model=List[PostResponse])
def get_posts():
    """Listar posts (público)"""
    return [PostResponse(**post) for post in posts]

@app.get("/posts/my", response_model=List[PostResponse])
def get_my_posts(current_user: User = Depends(auth.get_current_user)):
    """Obtener mis posts (requiere autenticación)"""
    my_posts = [post for post in posts if post["author"] == current_user.username]
    return [PostResponse(**post) for post in my_posts]

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, current_user: User = Depends(auth.get_current_user)):
    """Borrar post (solo el autor)"""
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    if post["author"] != current_user.username:
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar este post")
    posts.remove(post)
    return {"message": "Post eliminado exitosamente"}

@app.post("/create-admin", response_model=UserResponse)
def create_first_admin(user_data: UserCreate, db: Session = Depends(get_db)):
    """Crear primer usuario administrador"""
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Ya existe un administrador en el sistema")
    if auth.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username ya está registrado")
    admin_user = auth.create_admin_user(db, user_data.username, user_data.email, user_data.password)
    return UserResponse(id=admin_user.id, username=admin_user.username, email=admin_user.email, is_active=admin_user.is_active, role=admin_user.role)

@app.get("/admin/users", response_model=List[UserResponse])
def list_all_users(admin_user: User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    """Listar todos los usuarios (solo admin)"""
    users = auth.get_all_users(db)
    return [UserResponse(id=user.id, username=user.username, email=user.email, is_active=user.is_active, role=user.role) for user in users]

@app.put("/admin/users/{user_id}/role", response_model=UserResponse)
def update_user_role(user_id: int, role_data: UserRoleUpdate, admin_user: User = Depends(auth.require_admin), db: Session = Depends(get_db)):
    """Actualizar role de un usuario (solo admin)"""
    if user_id == admin_user.id:
        raise HTTPException(status_code=400, detail="No puedes cambiar tu propio rol")
    updated_user = auth.update_user_role(db, user_id, role_data.role)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserResponse(id=updated_user.id, username=updated_user.username, email=updated_user.email, is_active=updated_user.is_active, role=updated_user.role)