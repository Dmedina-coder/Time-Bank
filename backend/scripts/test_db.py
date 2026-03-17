import sys
from pathlib import Path

# Asegurar que la carpeta "backend" esté en sys.path cuando se ejecuta desde scripts/
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db import engine
from sqlalchemy import text


def main():
    insert_sql = """
        INSERT INTO users (name, email, password, role, balance)
        VALUES (:name, :email, :password, :role, :balance)
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            password = VALUES(password),
            role = VALUES(role),
            balance = VALUES(balance);
        """

    select_sql = """
    SELECT id, name, email, role, balance, created_at FROM users WHERE email = :email;
    """

    test_email = "test@example.com"

    # Usar engine.begin() para DDL/insert (se commitea automáticamente)
    with engine.begin() as conn:
        conn.execute(text(insert_sql), {
            "name": "Script Test User",
            "email": test_email,
            "password": "testpass",  # en tests solo
            "role": "user",
            "balance": 5,
        })

    # Leer y mostrar
    with engine.connect() as conn:
        result = conn.execute(text(select_sql), {"email": test_email})
        mappings = result.mappings().all()
        if not mappings:
            print("No se encontraron usuarios con ese email.")
            return
        for m in mappings:
            print(dict(m))


if __name__ == "__main__":
    main()
