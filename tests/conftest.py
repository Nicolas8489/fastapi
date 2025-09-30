import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base

# Base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_nutri.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# Fixture específica para Nutrición
@pytest.fixture
def sample_plan_data():
    """
    Datos de ejemplo específicos para Nutrición
    """
    return {
        "nombre_plan": "Plan Dietético Básico",
        "calorias_diarias": 1800,
        "duracion_semanas": 4,
        "tipo_dieta": "Baja en carbohidratos",
        "notas_nutricionales": "Incluir suplementos vitamínicos"
    }

@pytest.fixture
def auth_headers(client):
    """Headers de autenticación para tests"""
    response = client.post("/auth/register", json={
        "username": "admin_nutri",
        "password": "test123",
        "role": "nutricionista"  # Rol específico de Nutrición
    })

    login_response = client.post("/auth/login", data={
        "username": "admin_nutri",
        "password": "test123"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}