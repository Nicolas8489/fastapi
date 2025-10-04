# tests/test_tipo_d/test_basic_tipo_d.py
import pytest
from fastapi import status

@pytest.mark.tipo_d
@pytest.mark.unit
class TestCatalogoElementos:
    def test_crear_elemento_valido(self, client, sample_elemento_tipo_d, auth_headers):
        response = client.post(
            "/api/v1/joyas",
            json=sample_elemento_tipo_d,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nombre"] == sample_elemento_tipo_d["nombre"]
        assert data["categoria"] == sample_elemento_tipo_d["categoria"]
        assert "id" in data

    def test_obtener_elemento_existente(self, client, auth_headers):
        create_data = {
            "nombre": "Anillo GoldStyle",
            "categoria": "anillos",
            "precio": 150.50,
            "stock": 10,
            "sku": "AN01"
        }
        create_response = client.post(
            "/api/v1/joyas",
            json=create_data,
            headers=auth_headers
        )
        joya_id = create_response.json()["id"]
        response = client.get(f"/api/v1/joyas/{joya_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == joya_id
        assert data["nombre"] == create_data["nombre"]

    def test_listar_joyas_con_paginacion(self, client, auth_headers, pagination_params):
        response = client.get(
            "/api/v1/joyas",
            params=pagination_params,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert isinstance(data["items"], list)

    def test_actualizar_joya_existente(self, client, auth_headers):
        create_data = {
            "nombre": "Anillo Original",
            "categoria": "anillos",
            "precio": 150.50,
            "stock": 10,
            "sku": "AN01"
        }
        create_response = client.post(
            "/api/v1/joyas",
            json=create_data,
            headers=auth_headers
        )
        joya_id = create_response.json()["id"]
        update_data = {"precio": 200.00, "stock": 5}
        response = client.put(
            f"/api/v1/joyas/{joya_id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["precio"] == 200.00
        assert data["stock"] == 5

    def test_eliminar_joya_existente(self, client, auth_headers):
        create_data = {
            "nombre": "Anillo a Eliminar",
            "categoria": "anillos",
            "precio": 150.50,
            "stock": 10,
            "sku": "AN02"
        }
        create_response = client.post(
            "/api/v1/joyas",
            json=create_data,
            headers=auth_headers
        )
        joya_id = create_response.json()["id"]
        response = client.delete(f"/api/v1/joyas/{joya_id}", headers=auth_headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        get_response = client.get(f"/api/v1/joyas/{joya_id}", headers=auth_headers)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.tipo_d
@pytest.mark.unit
class TestValidacionesTipoD:
    def test_crear_joya_datos_invalidos(self, client, auth_headers):
        invalid_data = {
            "nombre": "",  # Nombre vacío
            "categoria": "x" * 101,  # Categoría muy larga
            "precio": -10.0,  # Precio inválido
            "stock": -5  # Stock inválido
        }
        response = client.post(
            "/api/v1/joyas",
            json=invalid_data,
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()["detail"]
        assert any("nombre" in str(error) or "precio" in str(error) or "stock" in str(error) for error in errors)

    def test_obtener_joya_inexistente(self, client, auth_headers):
        response = client.get("/api/v1/joyas/99999", headers=auth_headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrada" in response.json()["detail"].lower()
