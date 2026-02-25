"""
Main Application Entry Point
Punto de entrada principal de la aplicación
"""

from flask import Flask
from app.routes.api_routes import register_routes
from flask_cors import CORS

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    app.config['DATABASE_URI'] = 'sqlite:///timebank.db'
    
    # Habilitar CORS para el frontend
    CORS(app)
    
    # Registrar rutas
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
