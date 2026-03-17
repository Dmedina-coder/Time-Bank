# Time Bank - Banco de Tiempo

Plataforma web para intercambio de servicios entre usuarios usando una moneda virtual llamada **time credits**. Esta rama contiene el frontend en React y el backend en Python (Flask). El proyecto sigue arquitectura MVC, API REST y autenticación basada en JWT.

## Resumen del proyecto
- Usuarios ganan créditos al ofrecer servicios y gastan créditos al solicitar servicios.
- Soporta registro, login, publicación de servicios, solicitud/gestión de peticiones, transacciones de créditos y sistema de reseñas.

## Estructura del repositorio

```
Time_Bank/
├── backend/              # Backend en Python/Flask
│   ├── app/
│   │   ├── controllers/
│   │   ├── models/
│   │   ├── services/
│   │   ├── routes/
│   │   └── middleware/
│   ├── main.py
│   └── requirements.txt
└── frontend/             # Frontend en React
        ├── public/
        └── src/
```

## Tecnologías

- Frontend: React 18, React Router
- Backend: Python 3.x, Flask, PyJWT
- Base de datos: MySQL
- Autenticación: JWT

## Cómo ejecutar (rápido)

Backend (Windows):

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python main.py
```

Frontend:

```bash
cd frontend
npm install
npm start
```

## API — resumen de endpoints (extracto)

- Authentication
    - `POST /api/auth/register` — Registro (name, email, password)
    - `POST /api/auth/login` — Login (email, password) → devuelve `access_token`
    - `POST /api/auth/logout` — Logout (Authorization header)

- Users
    - `GET /api/users/me` — Perfil del usuario autenticado
    - `PUT /api/users/me` — Actualizar perfil
    - `GET /api/users` — Listado (admin)

- Services
    - `GET /api/services` — Listar
    - `POST /api/services` — Crear
    - `GET /api/services/{id}` — Obtener
    - `PUT /api/services/{id}` — Actualizar
    - `DELETE /api/services/{id}` — Eliminar

- Requests
    - `POST /api/requests` — Solicitar servicio
    - `PUT /api/requests/{id}/accept|reject|complete|cancel` — Cambiar estado

- Transactions
    - `GET /api/transactions` — Historial
    - `POST /api/transactions/transfer` — Transferir créditos

- Reviews
    - `POST /api/reviews` — Crear reseña
    - `GET /api/services/{id}/reviews` — Obtener reseñas

Para detalles de request/response ver la documentación principal en `Time Bank – System Documentation.md`.

## Base de datos

El esquema de la base de datos se encuentra en `backend/schema.sql` (MySQL). Contiene las tablas principales: `users`, `services`, `requests`, `transactions`, `reviews`, `credit_logs`.
