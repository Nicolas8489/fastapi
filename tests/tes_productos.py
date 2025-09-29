import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)

def test_crear_producto_sin_categoria(client):
    response = client.post("/products/", json={"nombre": "Producto Test", "precio": 99.99, "descripcion": "Producto de prueba"})
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Producto Test"

# (Resto de las pruebas de test_productos.py aquí)