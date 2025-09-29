#!/usr/bin/env python3
"""
Script de verificación rápida del setup FastAPI
"""

import sys
import os
from pathlib import Path
import subprocess

def verificar_setup():
    print("🚀 VERIFICACIÓN DEL SETUP FASTAPI")
    print("=" * 50)

    # Verificar Python
    print(f"✅ Python version: {sys.version.split()[0]}")
    print(f"✅ Python path: {sys.executable}")

    # Verificar entorno virtual
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        print(f"✅ Entorno virtual activo: {venv}")
    else:
        print("⚠️  Entorno virtual no detectado")

    # Verificar directorio de trabajo
    print(f"✅ Directorio actual: {os.getcwd()}")

    # Verificar instalaciones
    try:
        import fastapi
        print(f"✅ FastAPI instalado: v{fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI NO instalado")
        return False

    try:
        import uvicorn
        print(f"✅ Uvicorn instalado: v{uvicorn.__version__}")
    except ImportError:
        print("❌ Uvicorn NO instalado")
        return False

    # Verificar archivos del proyecto (ajustado para la estructura app/)
    archivos_requeridos = ["app/main.py", "requirements.txt", "README.md", ".gitignore"]
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"✅ Archivo presente: {archivo}")
        else:
            print(f"⚠️  Archivo faltante: {archivo}")

    # Verificar configuración Git
    try:
        git_user = subprocess.check_output(
            ['git', 'config', 'user.name'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        git_email = subprocess.check_output(
            ['git', 'config', 'user.email'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        print(f"✅ Git configurado - Usuario: {git_user}")
        print(f"✅ Git configurado - Email: {git_email}")
    except:
        print("⚠️  Git no configurado localmente")

    print("\n📊 RESUMEN DEL SETUP:")
    print("✅ Setup básico completado")
    print("🚀 Listo para ejecutar: uvicorn app.main:app --reload")  # Ajustado para app/main.py
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("🔎 Verificación disponible en: http://localhost:8000/info/setup")

    return True

if __name__ == "__main__":
    verificar_setup()