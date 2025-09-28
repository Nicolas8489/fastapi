from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
import models, schemas

# FUNCIONES CRUD PARA CATEGORÍAS
def crear_categoria(db: Session, categoria: schemas.CategoriaCreate):
    """Crear una nueva categoría"""
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def obtener_categorias(db: Session):
    """Obtener todas las categorías"""
    return db.query(models.Categoria).all()

def obtener_categoria(db: Session, categoria_id: int):
    """Obtener categoría por ID"""
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

def obtener_categoria_con_productos(db: Session, categoria_id: int):
    """Obtener categoría con sus productos"""
    return db.query(models.Categoria).options(
        joinedload(models.Categoria.productos)
    ).filter(models.Categoria.id == categoria_id).first()

# FUNCIONES CRUD PARA PRODUCTOS (actualizadas)
def crear_producto(db: Session, producto: schemas.ProductoCreate):
    """Crear un nuevo producto"""
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def obtener_producto(db: Session, producto_id: int):
    """Obtener producto por ID"""
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def obtener_productos(db: Session, skip: int = 0, limit: int = 10):
    """Obtener lista de productos con paginación"""
    return db.query(models.Producto).offset(skip).limit(limit).all()

def obtener_productos_con_categoria(db: Session, skip: int = 0, limit: int = 10):
    """Obtener productos con información de categoría"""
    return db.query(models.Producto).options(
        joinedload(models.Producto.categoria)
    ).offset(skip).limit(limit).all()

def obtener_productos_por_categoria(db: Session, categoria_id: int):
    """Obtener productos de una categoría específica"""
    return db.query(models.Producto).filter(
        models.Producto.categoria_id == categoria_id
    ).all()

def buscar_productos(db: Session, busqueda: str):
    """Buscar productos por nombre o descripción"""
    return db.query(models.Producto).filter(
        or_(
            models.Producto.nombre.contains(busqueda),
            models.Producto.descripcion.contains(busqueda)
        )
    ).all()

def actualizar_producto(db: Session, producto_id: int, producto: schemas.ProductoUpdate):
    """Actualizar producto existente"""
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        # Solo actualizar campos que no sean None
        update_data = producto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto, field, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto

def eliminar_producto(db: Session, producto_id: int):
    """Eliminar producto"""
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto

def contar_productos(db: Session):
    """Contar total de productos"""
    return db.query(models.Producto).count()
    # Agregar después de tus funciones CRUD existentes
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
import models, schemas

# FUNCIONES CRUD PARA AUTORES
def crear_autor(db: Session, autor: schemas.AutorCreate):
    """Crear un nuevo autor"""
    db_autor = models.Autor(**autor.dict())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor

def obtener_autores(db: Session):
    """Obtener todos los autores"""
    return db.query(models.Autor).all()

def obtener_autor_con_libros(db: Session, autor_id: int):
    """Obtener autor con sus libros"""
    return db.query(models.Autor).options(
        joinedload(models.Autor.libros)
    ).filter(models.Autor.id == autor_id).first()

# FUNCIONES CRUD PARA LIBROS
def crear_libro(db: Session, libro: schemas.LibroCreate):
    """Crear un nuevo libro"""
    db_libro = models.Libro(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

def obtener_libros_con_autor(db: Session):
    """Obtener libros con información del autor"""
    return db.query(models.Libro).options(
        joinedload(models.Libro.autor)
    ).all()

def buscar_libros_por_titulo(db: Session, busqueda: str):
    """Buscar libros por título"""
    return db.query(models.Libro).filter(
        models.Libro.titulo.contains(busqueda)
    ).all()

def buscar_libros_por_autor(db: Session, nombre_autor: str):
    """Buscar libros por nombre del autor"""
    return db.query(models.Libro).join(models.Autor).filter(
        models.Autor.nombre.contains(nombre_autor)
    ).all()

def obtener_libros_por_precio(db: Session, precio_min: float, precio_max: float):
    """Obtener libros en rango de precio"""
    return db.query(models.Libro).filter(
        models.Libro.precio >= precio_min,
        models.Libro.precio <= precio_max
    ).all()

def contar_libros(db: Session):
    """Contar total de libros"""
    return db.query(models.Libro).count()

def contar_autores(db: Session):
    """Contar total de autores"""
    return db.query(models.Autor).count()
# Agregar después de tus funciones CRUD existentes
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
import models, schemas

# FUNCIONES CRUD PARA AUTORES
def crear_autor(db: Session, autor: schemas.AutorCreate):
    """Crear un nuevo autor"""
    db_autor = models.Autor(**autor.dict())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor

def obtener_autores(db: Session):
    """Obtener todos los autores"""
    return db.query(models.Autor).all()

def obtener_autor_con_libros(db: Session, autor_id: int):
    """Obtener autor con sus libros"""
    return db.query(models.Autor).options(
        joinedload(models.Autor.libros)
    ).filter(models.Autor.id == autor_id).first()

# FUNCIONES CRUD PARA LIBROS
def crear_libro(db: Session, libro: schemas.LibroCreate):
    """Crear un nuevo libro"""
    db_libro = models.Libro(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

def obtener_libros_con_autor(db: Session):
    """Obtener libros con información del autor"""
    return db.query(models.Libro).options(
        joinedload(models.Libro.autor)
    ).all()

def buscar_libros_por_titulo(db: Session, busqueda: str):
    """Buscar libros por título"""
    return db.query(models.Libro).filter(
        models.Libro.titulo.contains(busqueda)
    ).all()

def buscar_libros_por_autor(db: Session, nombre_autor: str):
    """Buscar libros por nombre del autor"""
    return db.query(models.Libro).join(models.Autor).filter(
        models.Autor.nombre.contains(nombre_autor)
    ).all()

def obtener_libros_por_precio(db: Session, precio_min: float, precio_max: float):
    """Obtener libros en rango de precio"""
    return db.query(models.Libro).filter(
        models.Libro.precio >= precio_min,
        models.Libro.precio <= precio_max
    ).all()

def contar_libros(db: Session):
    """Contar total de libros"""
    return db.query(models.Libro).count()

def contar_autores(db: Session):
    """Contar total de autores"""
    return db.query(models.Autor).count()