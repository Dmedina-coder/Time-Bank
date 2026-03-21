# Guía de Referencia de la API - Time Bank

Este documento proporciona una referencia rápida para todos los endpoints de la API del Time Bank.

**URL Base:** Todas las rutas de la API están prefijadas con `/api`.

**Autenticación:** Las rutas protegidas requieren un token JWT en la cabecera de autorización:
`Authorization: Bearer <tu_token_jwt>`

---

## 1. Autenticación (`/auth`)

### **1.1 Registrar un nuevo usuario**

- **Endpoint:** `POST /auth/register`
- **Descripción:** Crea una nueva cuenta de usuario.
- **Cuerpo de la Petición (`application/json`):**
  ```json
  {
    "name": "Nombre Apellido",
    "email": "usuario@ejemplo.com",
    "password": "una_contraseña_segura",
    "role": "user" 
  }
  ```
  - `name` (string, **requerido**): Nombre completo del usuario.
  - `email` (string, **requerido**): Dirección de correo electrónico única.
  - `password` (string, **requerido**): Contraseña con un mínimo de 8 caracteres.
  - `role` (string, opcional): Rol del usuario (`'user'` o `'admin'`). Por defecto es `'user'`.
- **Respuesta Exitosa (201 Created):**
  ```json
  {
    "id": 1,
    "name": "Nombre Apellido",
    "email": "usuario@ejemplo.com",
    "role": "user",
    "balance": 0,
    "created_at": "2026-03-21T10:00:00Z",
    "access_token": "ey..."
  }
  ```

### **1.2 Iniciar sesión**

- **Endpoint:** `POST /auth/login`
- **Descripción:** Autentica a un usuario y devuelve un token de acceso.
- **Cuerpo de la Petición (`application/json`):**
  ```json
  {
    "email": "usuario@ejemplo.com",
    "password": "una_contraseña_segura"
  }
  ```
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "access_token": "ey...",
    "token_type": "Bearer",
    "expires_in": 86400,
    "user": {
      "id": 1,
      "name": "Nombre Apellido",
      "email": "usuario@ejemplo.com",
      "role": "user",
      "balance": 0,
      "created_at": "2026-03-21T10:00:00Z"
    }
  }
  ```

### **1.3 Cerrar sesión**

- **Endpoint:** `POST /auth/logout`
- **Descripción:** Invalida la sesión del usuario. (Nota: Con JWT, el cliente simplemente debe destruir el token).
- **Autenticación:** **Requerida**.
- **Respuesta Exitosa (204 No Content):** No devuelve contenido.

---

## 2. Usuarios (`/users`)

### **2.1 Obtener datos del usuario actual**

- **Endpoint:** `GET /users/me`
- **Descripción:** Devuelve la información del usuario autenticado.
- **Autenticación:** **Requerida**.
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "id": 1,
    "name": "Nombre Apellido",
    "email": "usuario@ejemplo.com",
    "role": "user",
    "balance": 0,
    "created_at": "2026-03-21T10:00:00Z"
  }
  ```

### **2.2 Actualizar datos del usuario actual**

- **Endpoint:** `PUT /users/me`
- **Descripción:** Permite al usuario autenticado actualizar su propia información.
- **Autenticación:** **Requerida**.
- **Cuerpo de la Petición (`application/json`):**
  - Todos los campos son opcionales.
  ```json
  {
    "name": "Nuevo Nombre",
    "email": "nuevo_email@ejemplo.com",
    "password": "nueva_contraseña_segura"
  }
  ```
- **Respuesta Exitosa (200 OK):** Devuelve el objeto del usuario actualizado.

### **2.3 Obtener datos de un usuario por ID**

- **Endpoint:** `GET /users/<user_id>`
- **Descripción:** Devuelve la información pública de un usuario específico.
- **Autenticación:** **Requerida**.
- **Parámetros de URL:**
  - `user_id` (integer, **requerido**): El ID del usuario a consultar.
- **Respuesta Exitosa (200 OK):** Devuelve el objeto del usuario.

### **2.4 Actualizar un usuario por ID (Admin)**

- **Endpoint:** `PUT /users/<user_id>`
- **Descripción:** Permite a un administrador actualizar la información de cualquier usuario.
- **Autenticación:** **Requerida** (y rol de `admin`).
- **Cuerpo de la Petición (`application/json`):**
  - Todos los campos son opcionales.
  ```json
  {
    "name": "Nombre Modificado",
    "email": "email.modificado@ejemplo.com",
    "role": "admin",
    "balance": 100
  }
  ```
- **Respuesta Exitosa (200 OK):** Devuelve el objeto del usuario actualizado.

---

## 3. Administración (`/admin`)

### **3.1 Obtener todos los usuarios (Admin)**

- **Endpoint:** `GET /admin/users`
- **Descripción:** Devuelve una lista paginada de todos los usuarios del sistema.
- **Autenticación:** **Requerida** (y rol de `admin`).
- **Parámetros de Query (opcionales):**
  - `page` (int): Número de página.
  - `per_page` (int): Resultados por página.
  - `search` (string): Término de búsqueda por nombre o email.
- **Respuesta Exitosa (200 OK):**
  ```json
  {
    "items": [
      { "id": 1, "name": "Usuario Uno", "email": "uno@ejemplo.com", ... },
      { "id": 2, "name": "Usuario Dos", "email": "dos@ejemplo.com", ... }
    ],
    "total": 2,
    "page": 1,
    "per_page": 20
  }
  ```
