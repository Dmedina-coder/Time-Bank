# Time Bank - Frontend

Frontend desarrollado en React para la aplicación Time Bank.

## Estructura del Proyecto

```
frontend/
│
├── src/
│   ├── pages/           # Páginas de la aplicación
│   ├── components/      # Componentes reutilizables
│   ├── services/        # Servicios API
│   └── context/         # Context API
│
├── public/              # Archivos estáticos
└── package.json         # Dependencias del proyecto
```

## Instalación

1. Instalar dependencias:
```bash
npm install
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con la URL de tu backend
```

## Ejecución

### Modo desarrollo:
```bash
npm start
```

La aplicación estará disponible en `http://localhost:3000`

### Build para producción:
```bash
npm run build
```

## Características

### Páginas

- **LoginPage**: Inicio de sesión
- **RegisterPage**: Registro de usuarios
- **Dashboard**: Panel principal con balance y estadísticas
- **Services**: Listado y creación de servicios
- **ServiceDetails**: Detalles de un servicio específico
- **Requests**: Gestión de solicitudes
- **AdminPanel**: Panel de administración

### Componentes

- **Navbar**: Barra de navegación
- **ServiceCard**: Tarjeta de servicio
- **ReviewComponent**: Componente de reseña
- **ProtectedRoute**: Rutas protegidas con autenticación

### Servicios

- **api.js**: Cliente HTTP para interactuar con el backend

### Context

- **AuthContext**: Gestión del estado de autenticación

## Tecnologías

- React 18
- React Router DOM 6
- Context API para manejo de estado
- CSS Modules
- Fetch API para peticiones HTTP

## Scripts Disponibles

- `npm start` - Inicia el servidor de desarrollo
- `npm run build` - Crea el build de producción
- `npm test` - Ejecuta los tests
- `npm run eject` - Expone la configuración de webpack

## Variables de Entorno

- `REACT_APP_API_URL` - URL del backend (default: http://localhost:5000/api)
