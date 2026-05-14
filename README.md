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
npm run dev
```

## API — resumen de endpoints (extracto)

- **Authentication**
    - `POST /api/auth/register` — Registro (name, email, password)
    - `POST /api/auth/login` — Login (email, password) → devuelve `access_token`
    - `POST /api/auth/logout` — Logout (Authorization header)

- **Users**
    - `GET /api/users/me` — Perfil del usuario autenticado
    - `PUT /api/users/me` — Actualizar perfil
    - `GET /api/users/{user_id}` — Obtener perfil público de un usuario

- **Services**
    - `GET /api/services` — Listar
    - `POST /api/services` — Crear
    - `GET /api/services/{id}` — Obtener
    - `PUT /api/services/{id}` — Actualizar
    - `DELETE /api/services/{id}` — Eliminar
    - `POST /api/services/{id}/image` — Subir imagen de servicio

- **Requests**
    - `POST /api/requests` — Solicitar servicio
    - `GET /api/requests` — Listar solicitudes del usuario
    - `PUT /api/requests/{id}/accept|reject|complete|cancel` — Cambiar estado
    - `GET /api/requests/{id}/messages` — Ver mensajes de una solicitud
    - `POST /api/requests/{id}/messages` — Enviar un mensaje

- **Transactions & Payments**
    - `GET /api/transactions` — Historial de transacciones del usuario
    - `POST /api/transactions/transfer` — Transferir créditos a otro usuario
    - `POST /api/payments/stripe/payment-intent` — Crear intento de pago para comprar créditos

- **Reviews**
    - `POST /api/reviews` — Crear reseña para un servicio completado
    - `GET /api/services/{id}/reviews` — Obtener reseñas de un servicio

- **Admin**
    - `GET /api/admin/users` — Listado de todos los usuarios
    - `POST /api/admin/users/{user_id}/credits` — Ajustar créditos de un usuario
    - `PUT /api/admin/services/{service_id}/approve|reject` — Aprobar o rechazar un servicio

Para detalles de request/response ver la documentación completa en `API_Reference.md`.

## Base de datos

El esquema de la base de datos se encuentra en `backend/schema.sql` (MySQL). Contiene las tablas principales: `users`, `services`, `requests`, `transactions`, `reviews`, `credit_logs`.
