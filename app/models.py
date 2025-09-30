from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    descripcion = Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="productos")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

    # app/models.py (agrega esto al final)
class Plan(Base):
    __tablename__ = "nutriplans"

    id = Column(Integer, primary_key=True, index=True)
    nombre_plan = Column(String, index=True)
    calorias_diarias = Column(Float)
    duracion_semanas = Column(Integer)
    tipo_dieta = Column(String)
    notas_nutricionales = Column(String)
    usuario_id = Column(Integer, ForeignKey("users.id"))
    usuario = relationship("User", back_populates="planes")