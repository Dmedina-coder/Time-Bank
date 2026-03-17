from flask import Flask
from flask_cors import CORS
from app.routes.api_routes import register_routes
from app.config import Config
from app.db import SessionLocal, init_db
from flask import g


def create_app():
    """Crea y configura la aplicación Flask usando la configuración desde .env"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar base de datos (crea tablas si hay modelos declarativos)
    try:
        init_db()
    except Exception:
        # En caso de que no haya modelos declarativos aún, ignorar
        pass

    # Habilitar CORS para el frontend
    CORS(app)

    # Registrar rutas
    register_routes(app)

    # Crear y cerrar sesión por request (SQLAlchemy puro)
    @app.before_request
    def _open_db():
        g.db = SessionLocal()

    @app.teardown_request
    def _close_db(exc):
        db = getattr(g, 'db', None)
        if db is None:
            return
        try:
            if exc:
                db.rollback()
            else:
                db.commit()
        finally:
            db.close()

    return app


if __name__ == '__main__':
    app = create_app()
    # Ejecutar la app; usar puerto configurable desde .env (PORT)
    app.run(debug=True, host='0.0.0.0', port=int(app.config.get('PORT', 5000)))
