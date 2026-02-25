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
- `DELETE /api/services/:id` - Eliminar servicio

### Solicitudes
- `GET /api/requests` - Listar solicitudes
- `POST /api/requests` - Crear solicitud
- `GET /api/requests/:id` - Obtener solicitud

### Transacciones
- `GET /api/transactions` - Listar transacciones
- `GET /api/transactions/:id` - Obtener transacción

### Administración
- `GET /api/admin/stats` - Obtener estadísticas
- `GET /api/admin/users` - Listar todos los usuarios
