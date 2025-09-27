# 📌 Mi API FastAPI - Semana 2

## 🚀 Descripción
API desarrollada con **FastAPI**, mejorada respecto a la Semana 1 con:
- Type Hints
- Modelos Pydantic
- Endpoints POST
- Parámetros de ruta y query
- Response Models

---

## ✅ Checklist de Verificación (Ejercicio 1)

- [x] **Type hints** en funciones (`-> dict`, `name: str`, etc.)
- [x] **Modelo Pydantic** creado (`class Product(BaseModel): ...`)
- [x] **Endpoint POST** que recibe un modelo Pydantic
- [x] **Endpoint GET con ID** (`/products/{id}`)
- [x] **API funcionando** con `uvicorn main:app --reload`
- [x] **Documentación interactiva** visible en `/docs`

---

## 🛠️ Instalación y ejecución

```bash
# Instalar dependencias
pip install fastapi pydantic uvicorn

# Ejecutar servidor
uvicorn main:app --reload
