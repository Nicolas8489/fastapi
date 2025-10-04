# tests/conftest.py - Fixtures genéricas para Joyería Exclusiva GoldStyle (Tipo D)
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from app.main import app
from app.database import get_db, Base
from app.auth.auth_handler import create_access_token

# Configuración de base de datos de prueba
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./test_goldstyle.db"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)

fake = Faker()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    token_data = {"sub": "usuario_test_goldstyle"}
    token = create_access_token(token_data)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_user_generic():
    return {
        "username": "usuario_goldstyle_test",
        "email": "test@goldstyle.com",
        "password": "password123",
        "is_active": True
    }

@pytest.fixture
def sample_elemento_tipo_d():
    return {
        "nombre": fake.word() + "_joya",
        "descripcion": fake.text(max_nb_chars=200),
        "categoria": fake.random_element(["anillos", "collares", "pulseras", "relojes"]),
        "precio": round(fake.random.uniform(10.0, 1000.0), 2),
        "stock": fake.random_int(0, 100),
        "sku": fake.uuid4()[:8].upper(),
        "dimensiones": {
            "largo": fake.random.uniform(1.0, 10.0),
            "ancho": fake.random.uniform(1.0, 10.0),
            "alto": fake.random.uniform(1.0, 10.0)
        },
        "peso": fake.random.uniform(0.1, 5.0),
        "disponible": True
    }

@pytest.fixture
def sample_transaccion_tipo_d():
    return {
        "elemento_id": 1,
        "cantidad": fake.random_int(1, 10),
        "tipo_transaccion": fake.random_element(["compra", "venta", "devolucion"]),
        "precio_unitario": round(fake.random.uniform(10.0, 500.0), 2),
        "fecha_transaccion": fake.date_time_this_year().isoformat(),
        "metodo_pago": fake.random_element(["efectivo", "tarjeta", "transferencia"]),
        "referencia": fake.uuid4()
    }

@pytest.fixture
def pagination_params():
    return {
        "skip": 0,
        "limit": 10,
        "sort_by": "id",
        "sort_order": "asc"
    }

@pytest.fixture
def search_params():
    return {
        "query": fake.word(),
        "filters": {
            "disponible": True,
            "categoria": "anillos"
        }
    }
