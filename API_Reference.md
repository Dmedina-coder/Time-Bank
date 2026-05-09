# Time Bank API Reference

This document provides a quick reference for all Time Bank API endpoints.

**Base URL:** All API routes are prefixed with `/api`.

**Authentication:** Protected routes require a JWT token in the authorization header:
`Authorization: Bearer <your_jwt_token>`

---

## 1. Authentication (`/auth`)

### **1.1 Register a New User**

- **Endpoint:** `POST /auth/register`
- **Description:** Creates a new user account.
- **Request Body (`application/json`):**
  ```json
  {
    "name": "First Last",
    "email": "user@example.com",
    "password": "a_secure_password",
    "role": "user"
  }
  ```
  - `name` (string, **required**): Full user name.
  - `email` (string, **required**): Unique email address.
  - `password` (string, **required**): Password with at least 8 characters.
  - `role` (string, optional): User role (`user` or `admin`). Defaults to `user`.
- **Success Response (201 Created):**
  ```json
  {
    "id": 1,
    "name": "First Last",
    "email": "user@example.com",
    "role": "user",
    "balance": 0,
    "created_at": "2026-03-21T10:00:00Z",
    "access_token": "ey..."
  }
  ```

### **1.2 Log In**

- **Endpoint:** `POST /auth/login`
- **Description:** Authenticates a user and returns an access token.
- **Request Body (`application/json`):**
  ```json
  {
    "email": "user@example.com",
    "password": "a_secure_password"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "access_token": "ey...",
    "token_type": "Bearer",
    "expires_in": 86400,
    "user": {
      "id": 1,
      "name": "First Last",
      "email": "user@example.com",
      "role": "user",
      "balance": 0,
      "created_at": "2026-03-21T10:00:00Z"
    }
  }
  ```

### **1.3 Log Out**

- **Endpoint:** `POST /auth/logout`
- **Description:** Invalidates the user session. (Note: with JWT, the client simply needs to discard the token.)
- **Authentication:** **Required**.
- **Success Response (200 OK):**
  ```json
  {
    "message": "Logout successful"
  }
  ```

---

## 2. Users (`/users`)

### **2.1 Get Current User**

- **Endpoint:** `GET /users/me`
- **Description:** Returns the authenticated user's information.
- **Authentication:** **Required**.
- **Success Response (200 OK):**
  ```json
  {
    "id": 1,
    "name": "First Last",
    "email": "user@example.com",
    "role": "user",
    "balance": 0,
    "created_at": "2026-03-21T10:00:00Z"
  }
  ```

### **2.2 Update Current User**

- **Endpoint:** `PUT /users/me`
- **Description:** Allows the authenticated user to update their own information.
- **Authentication:** **Required**.
- **Request Body (`application/json`):**
  - All fields are optional.
  ```json
  {
    "name": "New Name",
    "email": "new_email@example.com",
    "password": "new_secure_password"
  }
  ```
- **Success Response (200 OK):** Returns the updated user object.

### **2.3 Get User by ID**

- **Endpoint:** `GET /users/<user_id>`
- **Description:** Returns the public information of a specific user.
- **Authentication:** **Required**.
- **URL Parameters:**
  - `user_id` (integer, **required**): The ID of the user to retrieve.
- **Success Response (200 OK):** Returns the user object.

### **2.4 Update User by ID (Admin)**

- **Endpoint:** `PUT /users/<user_id>`
- **Description:** Allows an administrator to update any user's information.
- **Authentication:** **Required** (and `admin` role).
- **Request Body (`application/json`):**
  - All fields are optional.
  ```json
  {
    "name": "Modified Name",
    "email": "modified.email@example.com",
    "role": "admin",
    "balance": 100
  }
  ```
- **Success Response (200 OK):** Returns the updated user object.

---

## 3. Administration (`/admin`)

### **3.1 Get System Statistics (Admin)**

- **Endpoint:** `GET /admin/stats`
- **Description:** Returns a summary of the system state.
- **Authentication:** **Required** (and `admin` role).
- **Success Response (200 OK):**
  ```json
  {
    "users": {
      "total": 10,
      "admins": 2
    },
    "services": {
      "by_status": {
        "active": 8,
        "inactive": 1,
        "deleted": 1
      }
    },
    "requests": {
      "by_status": {
        "pending": 3,
        "accepted": 2
      }
    },
    "transactions": {
      "total": 14,
      "credits_sum": 120
    }
  }
  ```

### **3.2 Get All Users (Admin)**

- **Endpoint:** `GET /admin/users`
- **Description:** Returns a paginated list of all users in the system.
- **Authentication:** **Required** (and `admin` role).
- **Query Parameters (optional):**
  - `page` (int): Page number.
  - `per_page` (int): Results per page.
  - `search` (string): Search term by name or email.
- **Success Response (200 OK):**
  ```json
  {
    "items": [
      { "id": 1, "name": "User One", "email": "one@example.com", "role": "user", "balance": 10 },
      { "id": 2, "name": "User Two", "email": "two@example.com", "role": "admin", "balance": 40 }
    ]
  }
  ```

### **3.3 Adjust User Credits (Admin)**

- **Endpoint:** `POST /admin/users/<user_id>/credits`
- **Description:** Adds or subtracts credits from a user's balance and records the operation as a system transaction.
- **Authentication:** **Required** (and `admin` role).
- **Request Body (`application/json`):**
  ```json
  {
    "amount": 25
  }
  ```
- `amount` can be positive or negative, but it cannot be 0.
- **Success Response (200 OK):**
  ```json
  {
    "message": "Credits adjusted successfully",
    "user": {
      "id": 1,
      "name": "First Last",
      "email": "user@example.com",
      "role": "user",
      "balance": 25
    },
    "adjustment": 25,
    "new_balance": 25
  }
  ```

### **3.4 Approve a Service (Admin)**

- **Endpoint:** `PUT /admin/services/<service_id>/approve`
- **Description:** Changes the service status to `active`.
- **Authentication:** **Required** (and `admin` role).

### **3.5 Reject a Service (Admin)**

- **Endpoint:** `PUT /admin/services/<service_id>/reject`
- **Description:** Changes the service status to `inactive`.
- **Authentication:** **Required** (and `admin` role).

---

## 4. Services (`/services`)

### **4.1 List Services**

- **Endpoint:** `GET /services`
- **Description:** Returns a paginated list of visible services.
- **Authentication:** Not required.
- **Query Parameters (optional):**
  - `page` (int): Page number.
  - `per_page` (int): Results per page.
  - `category` (string): Filter by category.
  - `search` (string): Search by title or description.
  - `status` (string): Filter by status (`active`, `inactive`, `deleted`).

### **4.2 Create Service**

- **Endpoint:** `POST /services`
- **Description:** Creates a new service.
- **Authentication:** **Required**.
- **Request Body (`application/json`):**
  ```json
  {
    "title": "Math tutoring",
    "description": "Support for secondary school students",
    "category": "education",
    "credits": 3
  }
  ```

### **4.3 Get Service by ID**

- **Endpoint:** `GET /services/<service_id>`
- **Description:** Returns the details of a specific service.
- **Authentication:** Not required.

### **4.4 Update Service**

- **Endpoint:** `PUT /services/<service_id>`
- **Description:** Allows updating the title, description, category, credits, or status of the service.
- **Authentication:** **Required**.

### **4.5 Upload Service Image**

- **Endpoint:** `POST /services/<service_id>/image`
- **Description:** Stores an image associated with the service.
- **Authentication:** **Required**.
- **Content Type:** `multipart/form-data`
- **Required Field:**
  - `image` (file)

### **4.6 Get Service Image**

- **Endpoint:** `GET /services/<service_id>/image`
- **Description:** Returns the stored binary image for the service.
- **Authentication:** Not required.

### **4.7 Delete Service**

- **Endpoint:** `DELETE /services/<service_id>`
- **Description:** Marks the service as deleted.
- **Authentication:** **Required**.

---

## 5. Requests (`/requests`)

### **5.1 List Requests**

- **Endpoint:** `GET /requests`
- **Description:** Returns the requests visible to the authenticated user, with pagination.
- **Authentication:** **Required**.
- **Query Parameters (optional):**
  - `page` (int): Page number.
  - `per_page` (int): Results per page.
  - `status` (string): Filter by status.
  - `service_id` (int): Filter by service.

### **5.2 Create Request**

- **Endpoint:** `POST /requests`
- **Description:** Creates a new request for a service.
- **Authentication:** **Required**.
- **Request Body (`application/json`):**
  ```json
  {
    "service_id": 10,
    "scheduled_date": "2026-05-08T18:30:00Z"
  }
  ```
- **Notes:** `scheduled_date` must be in ISO 8601 format. The backend automatically assigns the provider based on the service owner.

### **5.3 Get Request**

- **Endpoint:** `GET /requests/<request_id>`
- **Description:** Returns the details of a request.
- **Authentication:** **Required**.

### **5.4 Update Request**

- **Endpoint:** `PUT /requests/<request_id>`
- **Description:** Allows updating `scheduled_date` or `status`.
- **Authentication:** **Required**.
- **Request Body (`application/json`):**
  ```json
  {
    "scheduled_date": "2026-05-10T10:00:00Z",
    "status": "accepted"
  }
  ```

### **5.5 Cancel Request**

- **Endpoint:** `PUT /requests/<request_id>/cancel`
- **Description:** Cancels an active request.
- **Authentication:** **Required**.

### **5.6 Accept Request**

- **Endpoint:** `PUT /requests/<request_id>/accept`
- **Description:** Marks the request as `accepted`.
- **Authentication:** **Required**.

### **5.7 Reject Request**

- **Endpoint:** `PUT /requests/<request_id>/reject`
- **Description:** Marks the request as `rejected`.
- **Authentication:** **Required**.

### **5.8 Complete Request**

- **Endpoint:** `PUT /requests/<request_id>/complete`
- **Description:** Marks the request as `completed` and, if applicable, automatically transfers credits between requester and provider.
- **Authentication:** **Required**.

### **5.9 Request Messaging**

- **Endpoint:** `GET /requests/<request_id>/messages`
- **Description:** Lists the messages for a request with pagination.
- **Authentication:** **Required**.
- **Query Parameters (optional):**
  - `page` (int): Page number.
  - `per_page` (int): Results per page.

- **Endpoint:** `POST /requests/<request_id>/messages`
- **Description:** Sends a message within the request.
- **Authentication:** **Required**.
- **Request Body (`application/json`):**
  ```json
  {
    "content": "Hi, does Tuesday at 5:00 PM work for you?"
  }
  ```

- **Endpoint:** `PUT /requests/<request_id>/messages/<message_id>/read`
- **Description:** Marks a message as read.
- **Authentication:** **Required**.

---

## 6. Transactions and Payments (`/transactions`, `/payments`)

### **6.1 List Transactions**

- **Endpoint:** `GET /transactions`
- **Description:** Returns the transactions visible to the authenticated user, with pagination.
- **Authentication:** **Required**.
- **Query Parameters (optional):**
  - `page` (int): Page number.
  - `per_page` (int): Results per page.
  - `type` (string): Filter by type (`transfer`, `purchase`, `refund`, `system`).

### **6.2 Get Transaction by ID**

- **Endpoint:** `GET /transactions/<transaction_id>`
- **Description:** Returns the details of a transaction.
- **Authentication:** **Required**.

### **6.3 Transfer Credits**

- **Endpoint:** `POST /transactions/transfer`
- **Description:** Creates a transaction between users.
- **Authentication:** **Required**.
- **Request Body (`application/json`):**
  ```json
  {
    "receiver_id": 2,
    "credits": 5,
    "type": "transfer"
  }
  ```

### **6.4 Get User Transactions**

- **Endpoint:** `GET /transactions/user/<user_id>`
- **Description:** Returns all transactions for a specific user.
- **Authentication:** **Required**.

### **6.5 Get Stripe Public Configuration**

- **Endpoint:** `GET /payments/stripe/config`
- **Description:** Returns the public configuration needed by the frontend.
- **Authentication:** **Required**.

### **6.6 Create Stripe PaymentIntent**

- **Endpoint:** `POST /payments/stripe/payment-intent`
- **Description:** Creates a PaymentIntent for buying credits.
- **Authentication:** **Required**.
- **Request Body (`application/json`):**
  ```json
  {
    "credits": 10,
    "currency": "usd"
  }
  ```

### **6.7 Confirm Stripe Payment**

- **Endpoint:** `POST /payments/stripe/confirm`
- **Description:** Confirms a successful payment and credits the user.
- **Authentication:** **Required**.
- **Request Body (`application/json`):**
  ```json
  {
    "payment_intent_id": "pi_123"
  }
  ```

---

## 7. Reviews (`/reviews`)

### **7.1 Create Review**

- **Endpoint:** `POST /reviews`
- **Description:** Creates a review for a completed service.
- **Authentication:** **Required** (only the requester of a completed service).
- **Request Body (`application/json`):**
  ```json
  {
    "service_id": 10,
    "request_id": 25,
    "rating": 5,
    "comment": "Great service, punctual and clear"
  }
  ```
  - `service_id` (int, **required**): ID of the reviewed service.
  - `request_id` (int, **required**): ID of the associated completed request.
  - `rating` (int, **required**): Rating from 1 to 5.
  - `comment` (string, optional): Free-form review comment.
- **Success Response (201 Created):** Returns the created review object.
