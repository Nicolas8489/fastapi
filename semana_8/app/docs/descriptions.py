# app/docs/descriptions.py
TAGS_METADATA = [
    {"name": "joyas", "description": "Operaciones CRUD para joyas de GoldStyle"},
    {"name": "sistema", "description": "Estado y salud de la API"},
]
ENDPOINT_DESCRIPTIONS = {
    "crear_joya": "### Crear Nueva Joya\nCrea una joya con SKU único y validaciones.",
    "obtener_joya": "### Obtener Joya por SKU\nRecupera detalles de una joya específica.",
}
RESPONSE_DESCRIPTIONS = {200: "Operación exitosa", 404: "Joya no encontrada"}
