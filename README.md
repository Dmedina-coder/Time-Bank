# Time Bank - Banco de Tiempo

Aplicación web para intercambio de servicios basado en tiempo, desarrollada con arquitectura MVC.

## Estructura del Proyecto

```
Time_Bank/
│
├── backend/              # Backend en Python/Flask
│   ├── app/
│   │   ├── controllers/  # Controladores
│   │   ├── models/       # Modelos de datos
│   │   ├── services/     # Lógica de negocio
│   │   ├── routes/       # Rutas de la API
│   │   └── middleware/   # Middlewares
│   ├── main.py          # Punto de entrada
│   └── requirements.txt # Dependencias Python
│
└── frontend/            # Frontend en React
    ├── src/
    │   ├── pages/       # Páginas de la aplicación
    │   ├── components/  # Componentes reutilizables
    │   ├── services/    # Servicios API
    │   └── context/     # Context API
    └── package.json     # Dependencias Node.js
```

## Tecnologías

### Backend
- Python 3.x
- Flask
- Flask-CORS
- PyJWT
- SQLAlchemy

### Frontend
- React 18
- React Router DOM 6
- Context API
- CSS3

## Instalación

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Configurar variables de entorno en .env
python main.py
```

El backend estará disponible en `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Configurar variables de entorno en .env
npm start
```

El frontend estará disponible en `http://localhost:3000`

## Funcionalidades

### Para Usuarios
- Registro e inicio de sesión
- Visualización de balance de tiempo
- Búsqueda y filtrado de servicios
- Creación de servicios propios
- Solicitud de servicios
- Gestión de solicitudes (aceptar/rechazar)
- Sistema de reseñas
- Historial de transacciones

### Para Administradores
- Panel de administración
- Estadísticas del sistema
- Gestión de usuarios
- Aprobación de servicios

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
- `PUT /api/requests/:id` - Actualizar solicitud

### Transacciones
- `GET /api/transactions` - Listar transacciones
- `GET /api/transactions/:id` - Obtener transacción

### Administración
- `GET /api/admin/stats` - Obtener estadísticas
- `GET /api/admin/users` - Listar todos los usuarios

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto.

## Contacto

Para preguntas y sugerencias, por favor abre un issue en el repositorio.
