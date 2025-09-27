Semana 3 - CRUD de Productos con FastAPI Avanzado
📌 Objetivo
Implementar un CRUD completo de productos usando FastAPI y Pydantic con validaciones avanzadas, manejo de errores profesional y funcionalidades de búsqueda. Los datos se almacenan en una base simulada en memoria.
✨ Características Avanzadas

✅ CRUD completo de productos
✅ Validaciones avanzadas con Pydantic
✅ Manejo de errores profesional con logging
✅ Búsqueda avanzada con filtros múltiples
✅ Documentación automática con Swagger UI
✅ Respuestas consistentes en formato JSON
✅ Query parameters validados automáticamente

📂 Estructura del proyecto
semana_3/
├── data/
│   └── products_data.py      # Base de datos simulada en memoria
├── models/
│   ├── __init__.py
│   └── product_models.py     # Modelos Pydantic básicos
├── main.py                   # Aplicación FastAPI completa
├── requirements.txt          # Dependencias del proyecto
└── README.md                # Esta documentación
🚀 Instalación y Ejecución
1. Preparar el entorno
bash# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
2. Ejecutar la aplicación
bash# Desde la carpeta semana_3/
uvicorn main:app --reload
3. Acceder a la API

API: http://127.0.0.1:8000
Documentación interactiva: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

📋 Dependencias (requirements.txt)
txtfastapi>=0.68.0
uvicorn[standard]>=0.15.0
pydantic>=1.8.0
python-multipart>=0.0.5