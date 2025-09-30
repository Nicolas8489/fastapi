import pytest
from fastapi.testclient import TestClient

def test_register_nutricion_user(client):
    """Test de registro específico para Nutrición"""
    data = {
        "username": "usuario_nutri_test",
        "password": "password123",
        "role": "nutricionista"  # Rol específico
    }

    response = client.post("/auth/register", json=data)
    assert response.status_code == 201

def test_login_nutricion_user(client):
    """Test de login específico para Nutrición"""
    register_data = {
        "username": "admin_nutri",
        "password": "admin123",
        "role": "nutricionista"
    }
    client.post("/auth/register", json=register_data)

    login_data = {
        "username": "admin_nutri",
        "password": "admin123"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()