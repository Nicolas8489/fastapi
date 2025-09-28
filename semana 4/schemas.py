from pydantic import BaseModel, validator
from typing import List, Optional

# Schemas para Categoría
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

# Schemas actualizados para Producto
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

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None

    @validator('precio')
    def validar_precio(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True

# Producto con información de categoría incluida
class ProductoConCategoria(ProductoBase):
    id: int
    categoria: Optional[Categoria] = None

    class Config:
        from_attributes = True

# Categoría con lista de productos
class CategoriaConProductos(Categoria):
    productos: List[ProductoBase] = []

    class Config:
        from_attributes = True