# Time Bank - Backend

Backend desarrollado en Python con Flask para la aplicación Time Bank.

## Estructura del Proyecto

```
backend/
│
├── app/
│   ├── controllers/      # Controladores de la aplicación
│   ├── models/          # Modelos de datos
│   ├── services/        # Lógica de negocio
│   ├── routes/          # Definición de rutas
│   └── middleware/      # Middlewares de la aplicación
│
├── main.py             # Punto de entrada de la aplicación
└── requirements.txt    # Dependencias del proyecto
```

## Instalación

1. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

## Ejecución

```bash
python main.py
```

La aplicación estará disponible en `http://localhost:5000`

## API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/logout` - Cerrar sesión

### Usuarios
- `GET /api/users/:id` - Obtener usuario
- `PUT /api/users/:id` - Actualizar usuario

### Servicios
- `GET /api/services` - Listar servicios
- `POST /api/services` - Crear servicio
- `GET /api/services/:id` - Obtener servicio
- `PUT /api/services/:id` - Actualizar servicio
- `POST /api/services/:id/image` - Subir imagen del servicio (multipart/form-data, campo `image`)
- `GET /api/services/:id/image` - Obtener imagen del servicio almacenada en DB
- `DELETE /api/services/:id` - Eliminar servicio

Para imágenes:
- Se almacenan en la base de datos en `services.image_data` (binario).
- Se guardan metadatos en `services.image_mime_type` y `services.image_filename`.

### Solicitudes
- `GET /api/requests` - Listar solicitudes
- `POST /api/requests` - Crear solicitud
- `GET /api/requests/:id` - Obtener solicitud
- `GET /api/requests/:id/messages` - Listar mensajes de una solicitud
- `POST /api/requests/:id/messages` - Enviar un mensaje en una solicitud
- `PUT /api/requests/:id/messages/:message_id/read` - Marcar un mensaje como leído

### Migración de mensajes
- `python scripts/add_request_messages.py` - Crea la tabla `request_messages` en bases ya existentes usando variables de entorno.

### Transacciones
- `GET /api/transactions` - Listar transacciones
- `GET /api/transactions/:id` - Obtener transacción

### Pagos (Stripe)
- `GET /api/payments/stripe/config` - Devuelve configuración pública de Stripe para frontend
- `POST /api/payments/stripe/payment-intent` - Crea un PaymentIntent para compra de créditos
- `POST /api/payments/stripe/confirm` - Confirma un PaymentIntent exitoso y acredita créditos

Variables de entorno opcionales para Stripe:
- `STRIPE_CURRENCY` (default: `eur`)
- `STRIPE_CREDIT_PRICE_CENTS` (default: `100`, equivale a 1.00 de moneda por crédito)

### Administración
- `GET /api/admin/stats` - Obtener estadísticas
- `GET /api/admin/users` - Listar todos los usuarios
