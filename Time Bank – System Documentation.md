# 1. Project Overview

## 1.1 Introduction

The **Time Bank Platform** is a web-based peer-to-peer system that enables users to exchange services using a virtual currency called **time credits**. Instead of paying with traditional money, users earn credits by providing services and spend them when requesting services from other users.

The system is designed to promote collaboration, knowledge sharing, and mutual support within a community. Each hour of service provided corresponds to a specific number of time credits that can later be used to obtain services from other participants.

The application will follow modern web engineering practices, including:
- MVC architecture
- RESTful API design
- Token-based authentication
- Secure communication between services
- Modular and scalable design
- Responsive frontend interface

The system will also support integration with an external payment provider that allows users to purchase time credits.

---
## 1.2 Objectives
The main objectives of the project are:
### Functional Objectives
- Allow users to register and manage their profiles.
- Enable users to offer services to the community.
- Allow users to search and request services.
- Implement a workflow for managing service requests.
- Manage a virtual currency system based on time credits.
- Track all credit transactions in the system.
- Allow users to review and rate completed services.
- Provide administrative tools for system moderation.
- Integrate an external payment gateway to purchase time credits.
### Technical Objectives
- Implement a scalable web application using MVC architecture.
- Separate frontend and backend responsibilities.
- Implement two independent backends:
    - Main application backend
    - Payment gateway backend
- Ensure secure authentication using JWT tokens.
- Provide a clean and documented REST API.
- Maintain code quality through modular design.
---
## 1.3 System Scope
The system will cover the following areas:

### User Management
Users can create accounts, authenticate, manage their profiles, and participate in service exchanges.

### Service Marketplace
Users can publish services they offer and discover services offered by others.

### Service Requests Workflow
Users can request services and providers can manage those requests.

### Virtual Economy
The system manages a virtual currency (time credits) used to pay for services.

### Payment Integration
Users can optionally buy time credits through an external payment provider.

### Administration
Administrators oversee platform activity and moderate users and services.

---
# 2. Backend Structure (Python)

Suggested structure:

```
backend/              # Backend en Python/Flask
├── app/
│   ├── controllers/  # Controladores
│   ├── models/       # Modelos de datos
│   ├── services/     # Lógica de negocio
│   ├── routes/       # Rutas de la API
│   └── middleware/   # Middlewares
├── main.py          # Punto de entrada
└── requirements.txt # Dependencias Python
```

---
# 3. Frontend Structure (React)

```
frontend/            # Frontend en React
├── src/
│   ├── pages/       # Páginas de la aplicación
│   ├── components/  # Componentes reutilizables
│   ├── services/    # Servicios API
│   └── context/     # Context API
└── package.json     # Dependencias Node.js
```

---
# 4. Domain Model (Class Diagram)

```mermaid
classDiagram

class User {
    id
    name
    email
    password
    role
    balance
    created_at
}

class Service {
    id
    title
    description
    owner_id
    category
    status
    created_at
}

class Request {
    id
    service_id
    requester_id
    provider_id
    status
    scheduled_date
}

class Transaction {
    id
    sender_id
    receiver_id
    credits
    type
    created_at
}

class Review {
    id
    service_id
    reviewer_id
    rating
    comment
}

User --> Service
User --> Request
User --> Transaction
Service --> Request
Service --> Review
```

---
# 5. Database ER Diagram

```mermaid
erDiagram

USERS {
    int id PK
    string name
    string email
    string password
    string role
    int balance
}

SERVICES {
    int id PK
    string title
    string description
    int owner_id FK
    string category
    string status
}

REQUESTS {
    int id PK
    int service_id FK
    int requester_id FK
    int provider_id FK
    string status
}

TRANSACTIONS {
    int id PK
    int sender_id FK
    int receiver_id FK
    int credits
    string type
}

REVIEWS {
    int id PK
    int service_id FK
    int reviewer_id FK
    int rating
    string comment
}
```

---
# 6. API Design

## Authentication

Para cada endpoint se indican los atributos esperados en las llamadas (request) y los atributos devueltos (response). Todas las llamadas protegidas requieren el header `Authorization: Bearer <token>`.

- POST /api/auth/register
    - Request (application/json):
        - `name` (string, required)
        - `email` (string, required, email)
        - `password` (string, required, mínimo 8 caracteres)
        - `role` (string, optional, 'user'|'admin', default 'user')
    - Response 200 (application/json):
        - `id` (int)
        - `name` (string)
        - `email` (string)
        - `role` (string)
        - `balance` (int)
        - `created_at` (timestamp)
        - `access_token` (string, JWT)

- POST /api/auth/login
    - Request (application/json):
        - `email` (string, required)
        - `password` (string, required)
    - Response 200 (application/json):
        - `access_token` (string, JWT)
        - `token_type` (string, e.g. 'Bearer')
        - `expires_in` (int, seconds)
        - `user` (object)

- POST /api/auth/logout
    - Request: Authorization header con JWT
    - Response 204 No Content

---

## Users

- GET /api/users/me
    - Request: Authorization header con JWT
    - Response 200 (application/json): 
        - objeto `user`


- PUT /api/users/me
    - Request (application/json): campos a actualizar (todos opcionales):
        - `name` (string)
        - `email` (string)
        - `password` (string, si se cambia debe cumplir reglas)
        - `profile` (object): `phone`, `address`, `bio`, etc.
    - Response 200 (application/json): 
        - objeto `user` actualizado

- GET /api/users
    - Descripción: listado para administradores
    - Request: Authorization header con JWT (rol `admin`) y query params opcionales:
        - `page` (int, default 1)
        - `per_page` (int, default 20)
        - `search` (string, busca por nombre o email)
        - `sort` (string, e.g. 'created_at:desc')
    - Response 200 (application/json):
        - `items` (array de objetos `user`)

---

## Services

- POST /api/services
    - Request: Authorization header con JWT
    - Request body (application/json):
        - `title` (string, required)
        - `description` (string, required)
        - `category` (string, required)
    - Response 201 (application/json):
        - `id` (int)
        - `title` (string)
        - `description` (string)
        - `owner_id` (int)
        - `category` (string)
        - `status` (string, default 'active')
        - `created_at` (timestamp)

- GET /api/services
    - Request: query params opcionales:
        - `page` (int, default 1)
        - `per_page` (int, default 20)
        - `category` (string)
        - `search` (string, busca en título o descripción)
        - `sort` (string, e.g. 'created_at:desc')
    - Response 200 (application/json):
        - `items` (array de objetos con `id`, `title`, `description`, `owner_id`, `category`, `status`, `created_at`)
        - `total` (int)
        - `page` (int)
        - `per_page` (int)

- GET /api/services/{id}
    - Request: sin parámetros
    - Response 200 (application/json):
        - `id` (int)
        - `title` (string)
        - `description` (string)
        - `owner_id` (int)
        - `owner` (object: `id`, `name`, `email`)
        - `category` (string)
        - `status` (string)
        - `created_at` (timestamp)

- PUT /api/services/{id}
    - Request: Authorization header con JWT (solo el propietario del servicio)
    - Request body (application/json), campos opcionales:
        - `title` (string)
        - `description` (string)
        - `category` (string)
        - `status` (string, 'active'|'inactive'|'archived')
    - Response 200 (application/json): objeto `service` actualizado

- DELETE /api/services/{id}
    - Request: Authorization header con JWT (solo el propietario del servicio)
    - Response 204 No Content

---

## Requests

- POST /api/requests
    - Request: Authorization header con JWT
    - Request body (application/json):
        - `service_id` (int, required)
        - `scheduled_date` (datetime, required)
        - `message` (string, optional)
    - Response 201 (application/json):
        - `id` (int)
        - `service_id` (int)
        - `requester_id` (int)
        - `provider_id` (int)
        - `status` (string, default 'pending')
        - `scheduled_date` (datetime)
        - `message` (string)
        - `created_at` (timestamp)

- PUT /api/requests/{id}/accept
    - Request: Authorization header con JWT (solo el proveedor del servicio)
    - Request body (application/json):
        - `scheduled_date` (datetime, optional)
    - Response 200 (application/json):
        - objeto `request` con `status` = 'accepted'

- PUT /api/requests/{id}/reject
    - Request: Authorization header con JWT (solo el proveedor del servicio)
    - Request body (application/json):
        - `reason` (string, optional)
    - Response 200 (application/json):
        - objeto `request` con `status` = 'rejected'

- PUT /api/requests/{id}/complete
    - Request: Authorization header con JWT (solo el proveedor del servicio)
    - Request body (application/json):
        - `credits_used` (int, required)
    - Response 200 (application/json):
        - objeto `request` con `status` = 'completed'
    - Nota: Ejecuta automáticamente la transacción de créditos

- PUT /api/requests/{id}/cancel
    - Request: Authorization header con JWT (requester o provider)
    - Request body (application/json):
        - `reason` (string, optional)
    - Response 200 (application/json):
        - objeto `request` con `status` = 'cancelled'

---

## Transactions

- GET /api/transactions
    - Request: Authorization header con JWT
    - Request query params opcionales:
        - `page` (int, default 1)
        - `per_page` (int, default 20)
        - `type` (string, 'credit'|'debit'|'transfer')
        - `start_date` (datetime)
        - `end_date` (datetime)
        - `sort` (string, e.g. 'created_at:desc')
    - Response 200 (application/json):
        - `items` (array de objetos con `id`, `sender_id`, `receiver_id`, `credits`, `type`, `reason`, `created_at`)
        - `total` (int)
        - `page` (int)
        - `per_page` (int)
        - `balance` (int, saldo actual del usuario)

- POST /api/transactions/transfer
    - Request: Authorization header con JWT
    - Request body (application/json):
        - `receiver_id` (int, required)
        - `credits` (int, required, > 0)
        - `reason` (string, optional)
    - Response 201 (application/json):
        - `id` (int)
        - `sender_id` (int)
        - `receiver_id` (int)
        - `credits` (int)
        - `type` (string, 'transfer')
        - `reason` (string)
        - `created_at` (timestamp)

---

## Reviews

- POST /api/reviews
    - Request: Authorization header con JWT (solo el requester de un servicio completado)
    - Request body (application/json):
        - `service_id` (int, required)
        - `request_id` (int, required)
        - `rating` (int, required, 1-5)
        - `comment` (string, optional)
    - Response 201 (application/json):
        - `id` (int)
        - `service_id` (int)
        - `reviewer_id` (int)
        - `rating` (int)
        - `comment` (string)
        - `created_at` (timestamp)

- GET /api/services/{id}/reviews
    - Request: query params opcionales:
        - `page` (int, default 1)
        - `per_page` (int, default 10)
        - `sort` (string, e.g. 'created_at:desc'|'rating:desc')
    - Response 200 (application/json):
        - `items` (array de objetos con `id`, `service_id`, `reviewer_id`, `reviewer` (object: `id`, `name`), `rating`, `comment`, `created_at`)
        - `total` (int)
        - `page` (int)
        - `per_page` (int)
        - `average_rating` (float)

---
# 7. Payment Gateway Communication

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant PaymentGateway

    User->>Frontend: Buy Time Credits
    Frontend->>Backend: Create payment request
    Backend->>PaymentGateway: Payment initialization
    PaymentGateway-->>Backend: Payment confirmation (webhook)
    Backend->>Backend: Update user balance
    Backend-->>Frontend: Payment success
```


---
# 8. Use Case Diagram

```mermaid
flowchart TD
    User((User))
    Admin((Admin))

    Register[Register]
    Login[Login]
    CreateService[Create Service]
    RequestService[Request Service]
    CompleteService[Complete Service]
    BuyCredits[Buy Credits]
    ReviewService[Review Service]

    ManageUsers[Manage Users]
    ModerateServices[Moderate Services]
    MonitorTransactions[Monitor Transactions]

    User --> Register
    User --> Login
    User --> CreateService
    User --> RequestService
    User --> CompleteService
    User --> BuyCredits
    User --> ReviewService

    Admin --> ManageUsers
    Admin --> ModerateServices
    Admin --> MonitorTransactions
```

---
# 9. Navigation Model (Frontend)

```mermaid
flowchart TD
    A[Home] --"Click 'Login'"--> B(Login)
    A --"Click 'Register'"--> C(Register)
    
    B --"Successful Login"--> D{Dashboard}
    C --"Successful Registration"--> D

    D --"View Services"--> E[Services List]
    D --"View My Requests"--> F[My Requests]
    D --"View Transactions"--> G[My Transactions]
    D --"View Profile"--> H[My Profile]
    D --"Admin Access"--> I[Admin Panel]
    D --"Logout"--> A

    E --"Select a Service"--> L(Service Details)
    L --"Click 'Request Service'"--> M[Create Request Page]
    L --"Click Provider's Name"--> N[Provider's Profile]
    
    M --"Submit Request"--> F
    N --"Back to Service"--> L
    
    E --"Back to Dashboard"--> D
    F --"Back to Dashboard"--> D
    G --"Back to Dashboard"--> D
    H --"Back to Dashboard"--> D
    I --"Back to Dashboard"--> D
    L --"Back to Services"--> E
```

---
# 10. Security Model

Authentication method:

* JWT Tokens
* Token stored securely in frontend
* Middleware validation

Security measures:

* Password hashing (bcrypt)
* Input validation
* Role-based access control
* HTTPS
* Rate limiting

---
# 11. Sprint-Based Implementation Plan

## Sprint 1 — Foundations & Security

* Authentication system
* JWT implementation
* User management
* Basic API
* MVC architecture setup

## Sprint 2 — Core Platform

* Services marketplace
* Requests workflow
* Credits system
* Transactions
* Service discovery

## Sprint 3 — Advanced Features

* Payment gateway integration
* Reviews & ratings
* Admin panel
* Monitoring tools
