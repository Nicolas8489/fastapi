from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Literal

# Schemas para Categoría
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    productos: List["ProductoBase"] = []

    class Config:
        from_attributes = True

class CategoriaConProductos(Categoria):
    productos: List["ProductoBase"] = []

# Schemas para Producto
class ProductoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: str
    categoria_id: Optional[int] = None

    @validator('nombre')
    def validar_nombre(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

    @validator('precio')
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v

class ProductCreate(ProductoBase):
    pass

class ProductUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None

    @validator('precio')
    def validar_precio(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v

class ProductResponse(ProductoBase):
    id: int
    categoria: Optional[Categoria] = None

    class Config:
        from_attributes = True

# Schemas para Autenticación
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

class UserRoleUpdate(BaseModel):
    role: Literal["user", "admin"]

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str

    # app/schemas.py (agrega esto al final)
class PlanBase(BaseModel):
    nombre_plan: str
    calorias_diarias: float
    duracion_semanas: int
    tipo_dieta: str
    notas_nutricionales: Optional[str] = None

class PlanCreate(PlanBase):
    pass

class Plan(PlanBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True