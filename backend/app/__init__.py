from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

# Inicializar la extensión SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Crea y configura una instancia de la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la base de datos con la aplicación
    db.init_app(app)

    # Habilitar CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar las rutas de la API
    from .routes.api_routes import register_routes
    register_routes(app)

    return app