from fastapi import FastAPI

app = FastAPI(
    title="Mi Primera API - Semana 1",
    description="Bootcamp Semana 1 - Prácticas y ejercicios iniciales con FastAPI",
    version="1.0.0"
)

# -------------------------
# 👇 Aquí van las prácticas y ejercicios de la semana 1
# -------------------------

@app.get("/")
def read_root() -> dict:
    return {"mensaje": "🚀 Bienvenido a la Semana 1 de FastAPI"}

@app.get("/ejercicio")
def ejercicio() -> dict:
    return {"resultado": "✅ Este es el ejercicio de la Semana 1"}

# Endpoint especial de verificación
@app.get("/info/setup")
def info_setup() -> dict:
    return {
        "status": "ok",
        "message": "🚀 Setup FastAPI funcionando correctamente",
        "docs": "http://localhost:8000/docs",
        "server": "http://localhost:8000"
    }

# -------------------------
# 🚀 Punto de entrada principal
# -------------------------
if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor de verificación...")
    print("📌 Acceder a: http://localhost:8000")
    print("📖 Documentación: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
