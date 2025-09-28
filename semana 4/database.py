from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./productos.db"

# Crear engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

# Crear SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear Base class
Base = declarative_base()

# Dependencia para obtener DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()