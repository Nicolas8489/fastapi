# app/main.py
from fastapi import FastAPI
from .routers.joyas import router

app = FastAPI(title="Joyería Exclusiva GoldStyle API")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
