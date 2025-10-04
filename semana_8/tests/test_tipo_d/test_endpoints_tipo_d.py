# tests/test_tipo_d/test_endpoints_tipo_d.py
import pytest
from fastapi import status
from datetime import datetime, timedelta

@pytest.mark.tipo_d
@pytest.mark.integration
class TestJoyasEndpoints:
    def test_crud_completo_joya(self, authenticated_client, sample_elemento_tipo_d):
        create_response = authenticated_client.post(
            "/api/v1/joyas",
            json=sample_elemento_tipo_d
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_data = create_response.json()
        joya_id = created_data["id"]
        assert created_data["nombre"] == sample_elemento_tipo_d["nombre"]

        read_response = authenticated_client.get(f"/api/v1/joyas/{joya_id}")
        assert read_response.status_code == status.HTTP_200_OK

        update_data = {"precio": 300.00, "stock": 8}
        update_response = authenticated_client.put(
            f"/api/v1/joyas/{joya_id}",
            json=update_data
        )
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["precio"] == 300.00

        delete_response = authenticated_client.delete(f"/api/v1/joyas/{joya_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        verify_response = authenticated_client.get(f"/api/v1/joyas/{joya_id}")
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND

    def test_busqueda_avanzada_joyas(self, authenticated_client, sample_elemento_tipo_d):
        authenticated_client.post("/api/v1/joyas", json=sample_elemento_tipo_d)
        search_response = authenticated_client.get(
            "/api/v1/joyas/buscar",
            params={"categoria": "anillos", "disponible": True, "limit": 10}
        )
        assert search_response.status_code == status.HTTP_200_OK
        data = search_response.json()
        assert "items" in data
        for item in data["items"]:
            assert item["categoria"] == "anillos"
            assert item["disponible"] is True

    def test_paginacion_joyas(self, authenticated_client):
        for i in range(25):
            data = {"nombre": f"Joya {i}", "categoria": "anillos", "precio": 100.00, "stock": 10, "sku": f"JOY{i:02d}"}
            authenticated_client.post("/api/v1/joyas", json=data)
        page1_response = authenticated_client.get("/api/v1/joyas", params={"skip": 0, "limit": 10})
        assert page1_response.status_code == status.HTTP_200_OK
        page1_data = page1_response.json()
        assert len(page1_data["items"]) == 10
        assert page1_data["total"] >= 25

    def test_validaciones_negocio_joyas(self, authenticated_client, sample_elemento_tipo_d):
        authenticated_client.post("/api/v1/joyas", json=sample_elemento_tipo_d)
        duplicate_data = sample_elemento_tipo_d.copy()
        response = authenticated_client.post("/api/v1/joyas", json=duplicate_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "duplicado" in response.json()["detail"].lower()

@pytest.mark.tipo_d
@pytest.mark.unit
class TestValidacionesTipoD:
    def test_validacion_campos_requeridos(self, authenticated_client):
        invalid_data = {"descripcion": "Joya sin nombre", "categoria": "anillos"}
        response = authenticated_client.post("/api/v1/joyas", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        errors = response.json()["detail"]
        assert any("nombre" in str(error) for error in errors)

    def test_validacion_tipos_datos(self, authenticated_client):
        invalid_data = {
            "nombre": "Joya Test",
            "categoria": "anillos",
            "precio": "no_float",
            "stock": "no_int"
        }
        response = authenticated_client.post("/api/v1/joyas", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
