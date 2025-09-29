# app/__init__.py
from .main import app
from .database import get_db
from .models import Categoria, Product, User  # SQLAlchemy models
from .models.product_models import Product as PydanticProduct, ProductCreate, ProductUpdate  # Optional Pydantic models
from .schemas import CategoriaCreate, ProductCreate as SchemaProductCreate, UserCreate, UserResponse, Token
from .crud import crear_categoria, crear_producto, create_user
from .auth import hash_password, verify_password, create_access_token

__all__ = [
    "app",
    "get_db",
    "Categoria",
    "Product",
    "User",
    "PydanticProduct",
    "ProductCreate",
    "ProductUpdate",
    "CategoriaCreate",
    "SchemaProductCreate",
    "UserCreate",
    "UserResponse",
    "Token",
    "crear_categoria",
    "crear_producto",
    "create_user",
    "hash_password",
    "verify_password",
    "create_access_token",
]