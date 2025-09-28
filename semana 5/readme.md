# Semana 5 - Proyecto de Autenticación y Autorización

## 🎯 Objetivos Generales

Implementar un sistema completo de autenticación y autorización con JWT, hashing de contraseñas, protección de endpoints y roles básicos en 6 horas distribuidas en 5 prácticas (15, 16, 17, 18 y Ejercicios Prácticos).

## ⏱️ Tiempo Total Estimado

- Práctica 15: 90 minutos
- Práctica 16: 90 minutos
- Práctica 17: 90 minutos
- Práctica 18: 90 minutos
- Ejercicios Prácticos: 45 minutos
- **Total: 6 horas**

## 📋 Pre-requisitos

- ✅ SQLAlchemy configurado y funcional
- ✅ Modelos y operaciones CRUD básicas implementadas
- ✅ Conocimientos teóricos de autenticación y autorización

## 🚀 Desarrollo Consolidado

### Práctica 15: JWT y Hashing Básico
- **Objetivo**: Implementar autenticación básica con JWT y hashing de contraseñas.
- **Desarrollo**:
  - Instalar dependencias (`python-jose`, `passlib[bcrypt]`, `python-multipart`) en `requirements.txt`.
  - Configurar `auth.py` con funciones de hashing y JWT.
  - Crear `models.py` con un modelo `User`.
  - Definir esquemas en `schemas.py`.
  - Implementar endpoints básicos en `main.py` (registro, login, protegido).
- **Testing**: Prueba manual con curl y Swagger (`http://localhost:8000/docs`).

### Práctica 16: Endpoints de Login y Register
- **Objetivo**: Crear endpoints básicos de registro y login.
- **Desarrollo**:
  - Refinar `models.py` y `schemas.py` para usuarios.
  - Añadir funciones CRUD en `auth.py`.
  - Implementar endpoints `/register`, `/login` y `/users/me` en `main.py`.
- **Testing**: Verifica registro, login y acceso protegido.

### Práctica 17: Protección de Endpoints Básica
- **Objetivo**: Proteger endpoints con autenticación JWT.
- **Desarrollo**:
  - Completar `get_current_user` en `auth.py`.
  - Proteger endpoints existentes y añadir CRUD de posts en `main.py`.
- **Testing**: Prueba con y sin token, verifica errores 401/403.

### Práctica 18: Roles Básicos
- **Objetivo**: Implementar roles (admin/user).
- **Desarrollo**:
  - Añadir campo `role` a `models.py` y `schemas.py`.
  - Crear funciones de roles y endpoints de administración en `auth.py` y `main.py`.
- **Testing**: Crea un admin, verifica acceso denegado para usuarios normales.

### Ejercicios Prácticos - Semana 5
- **Objetivo**: Consolidar conocimientos.
- **Ejercicio 1**: Verifica funcionamiento (hashing, JWT, roles, etc.).
- **Ejercicio 2**: Crea un mini sistema de posts protegido.
- **Ejercicio 3**: Prueba seguridad (sin token, token inválido, roles).
- **Testing**: Usa curl para validar.

## 🧪 Testing Manual Consolidado

### Comandos de Ejemplo
- **Registrar usuario**:
  ```bash
  curl -X POST "http://127.0.0.1:8000/register" -H "Content-Type: application/json" -d '{"username": "juan", "email": "juan@test.com", "password": "password123"}'