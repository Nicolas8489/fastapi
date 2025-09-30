import pytest
from fastapi.testclient import TestClient

class TestNutricionAPI:
    """Tests específicos para Nutrición - FICHA 3147246"""

    def test_create_plan_success(self, client, sample_plan_data, auth_headers):
        """Test de creación exitosa de plan en Nutrición"""
        response = client.post(
            "/nutriplans/",
            json=sample_plan_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["nombre_plan"] == sample_plan_data["nombre_plan"]
        assert "id" in data

    def test_create_plan_duplicate(self, client, sample_plan_data, auth_headers):
        """Test de creación duplicada en Nutrición"""
        client.post("/nutriplans/", json=sample_plan_data, headers=auth_headers)
        response = client.post("/nutriplans/", json=sample_plan_data, headers=auth_headers)
        assert response.status_code == 400
        assert "ya existe" in response.json()["detail"].lower()

    def test_get_plan_by_id(self, client, auth_headers):
        """Test de consulta por ID en Nutrición"""
        create_data = {"nombre_plan": "Plan de Pérdida de Peso", "calorias_diarias": 1500}
        create_response = client.post("/nutriplans/", json=create_data, headers=auth_headers)
        created_id = create_response.json()["id"]

        response = client.get(f"/nutriplans/{created_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id

    def test_get_all_plans(self, client, auth_headers):
        """Test de consulta de todos los planes en Nutrición"""
        response = client.get("/nutriplans/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_plan_not_found(self, client, auth_headers):
        """Test de plan no encontrado en Nutrición"""
        response = client.get("/nutriplans/999", headers=auth_headers)
        assert response.status_code == 404
        assert "plan no encontrado" in response.json()["detail"].lower()

    def test_update_plan_complete(self, client, auth_headers):
        """Test de actualización completa en Nutrición"""
        create_data = {"nombre_plan": "Plan Inicial", "calorias_diarias": 2000}
        create_response = client.post("/nutriplans/", json=create_data, headers=auth_headers)
        entity_id = create_response.json()["id"]

        update_data = {"nombre_plan": "Plan Actualizado", "calorias_diarias": 1800}
        response = client.put(f"/nutriplans/{entity_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        updated = response.json()
        assert updated["nombre_plan"] == "Plan Actualizado"

    def test_delete_plan_success(self, client, auth_headers):
        """Test de eliminación exitosa en Nutrición"""
        create_data = {"nombre_plan": "Plan a Eliminar", "calorias_diarias": 1600}
        create_response = client.post("/nutriplans/", json=create_data, headers=auth_headers)
        entity_id = create_response.json()["id"]

        response = client.delete(f"/nutriplans/{entity_id}", headers=auth_headers)
        assert response.status_code == 200

        get_response = client.get(f"/nutriplans/{entity_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_plan_business_rules(self, client, auth_headers):
        """Test de reglas de negocio específicas para Nutrición"""
        invalid_data = {
            "nombre_plan": "",
            "calorias_diarias": -100,  # Valor inválido
            "duracion_semanas": 0
        }

        response = client.post("/nutriplans/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("calorias_diarias" in str(error) for error in errors)
        assert any("duracion_semanas" in str(error) for error in errors)

    def test_create_plan_requires_auth(self, client):
        """Test que crear plan requiere autenticación"""
        data = {"nombre_plan": "Plan Sin Auth", "calorias_diarias": 1700}
        response = client.post("/nutriplans/", json=data)
        assert response.status_code == 401
def test_nutricionista_can_delete_plan(self, client, auth_headers):
    create_data = {"nombre_plan": "Plan a Eliminar", "calorias_diarias": 1600}
    create_response = client.post("/nutriplans/", json=create_data, headers=auth_headers)
    entity_id = create_response.json()["id"]
    response = client.delete(f"/nutriplans/{entity_id}", headers=auth_headers)
    assert response.status_code == 200

def test_regular_user_cannot_delete_plan(self, client):
    # Crear usuario regular
    client.post("/auth/register", json={"username": "user_nutri", "password": "test123", "role": "usuario"})
    login_response = client.post("/auth/login", data={"username": "user_nutri", "password": "test123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_data = {"nombre_plan": "Plan Protegido", "calorias_diarias": 1700}
    create_response = client.post("/nutriplans/", json=create_data, headers=headers)
    entity_id = create_response.json()["id"]
    response = client.delete(f"/nutriplans/{entity_id}", headers=headers)
    assert response.status_code == 403

    def test_update_plan_partial(self, client, auth_headers):
         """Test de actualización parcial para Nutrición"""
    create_data = {"nombre_plan": "Plan Inicial", "calorias_diarias": 2000}
    create_response = client.post("/nutriplans/", json=create_data, headers=auth_headers)
    entity_id = create_response.json()["id"]

    update_data = {"calorias_diarias": 1800}  # Solo un campo
    response = client.patch(f"/nutriplans/{entity_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    updated = response.json()
    assert updated["calorias_diarias"] == 1800