import pytest   
from fastapi.testclient import TestClient

def test_crear_categoria(client: TestClient):
    """Test crear una nueva categoría"""
    response = client.post(
        "/categorias/",
        json={"nombre": "Electrónicos", "descripcion": "Dispositivos electrónicos"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Electrónicos"
    assert data["descripcion"] == "Dispositivos electrónicos"
    assert "id" in data

def test_listar_categorias_vacio(client: TestClient):
    """Test listar categorías cuando no hay ninguna"""
    response = client.get("/categorias/")
    assert response.status_code == 200
    assert response.json() == []

def test_listar_categorias_con_datos(client: TestClient):
    """Test listar categorías con datos"""
    # Crear categoría
    client.post(
        "/categorias/",
        json={"nombre": "Libros", "descripcion": "Libros y literatura"}
    )

    # Listar categorías
    response = client.get("/categorias/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "Libros"

def test_obtener_categoria(client: TestClient):
    """Test obtener categoría específica"""
    # Crear categoría
    create_response = client.post(
        "/categorias/",
        json={"nombre": "Deportes", "descripcion": "Artículos deportivos"}
    )
    categoria_id = create_response.json()["id"]

    # Obtener categoría
    response = client.get(f"/categorias/{categoria_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Deportes"
    assert data["productos"] == []  # Sin productos inicialmente

def test_categoria_no_encontrada(client: TestClient):
    """Test error cuando categoría no existe"""
    response = client.get("/categorias/999")
    assert response.status_code == 404

def test_crear_categoria_nombre_vacio(client: TestClient):
    """Test validación de nombre vacío"""
    response = client.post(
        "/categorias/",
        json={"nombre": "", "descripcion": "Descripción válida"}
    )
    assert response.status_code == 422  # Validation error

def test_productos_por_categoria_vacia(client: TestClient):
    """Test obtener productos de categoría sin productos"""
    # Crear categoría
    create_response = client.post(
        "/categorias/",
        json={"nombre": "Categoría Vacía", "descripcion": "Sin productos"}
    )
    categoria_id = create_response.json()["id"]

    # Obtener productos de la categoría
    response = client.get(f"/categorias/{categoria_id}/productos/")
    assert response.status_code == 200
    data = response.json()
    assert data["categoria_id"] == categoria_id
    assert data["productos"] == []
    assert data["total"] == 0