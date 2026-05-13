"""
Migración: añade la columna is_active a la tabla users
Ejecutar una sola vez sobre la base de datos existente.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        db.session.execute(
            text("ALTER TABLE users ADD COLUMN is_active TINYINT(1) NOT NULL DEFAULT 1")
        )
        db.session.commit()
        print("Columna 'is_active' añadida correctamente a la tabla 'users'.")
    except Exception as e:
        if 'Duplicate column name' in str(e) or 'already exists' in str(e).lower():
            print("La columna 'is_active' ya existe. No se requiere migración.")
        else:
            print(f"Error durante la migración: {e}")
            sys.exit(1)
