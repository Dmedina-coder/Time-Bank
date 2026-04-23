"""
Script para crear un usuario administrador en la BD.
Usa el mismo algoritmo de hashing que la app (SHA-256 + salt).
"""
import hashlib
import pymysql

# ── Config ──────────────────────────────────────────────────────────────────
DB_HOST     = 'dmedinaserver.duckdns.org'
DB_PORT     = 3306
DB_USER     = 'TimeUser'
DB_PASSWORD = 'Tb2026-K9f8_rX'
DB_NAME     = 'timebank'

SALT        = 'yIMjALAt5n3N0C2oYOPlMd8n9s5X7v'   # valor de PASSWORD_HASH_SALT en .env

ADMIN_NAME  = 'Admin'
ADMIN_EMAIL = 'admin@timebank.com'
ADMIN_PASS  = 'Admin1234!'     # cámbialo si quieres
# ────────────────────────────────────────────────────────────────────────────

def hash_password(password):
    return hashlib.sha256((SALT + password).encode()).hexdigest()

conn = pymysql.connect(
    host=DB_HOST, port=DB_PORT,
    user=DB_USER, password=DB_PASSWORD,
    database=DB_NAME, charset='utf8mb4'
)
cur = conn.cursor()

# Comprobar si ya existe
cur.execute("SELECT id, role FROM users WHERE email = %s", (ADMIN_EMAIL,))
existing = cur.fetchone()

if existing:
    cur.execute("UPDATE users SET role = 'admin', name = %s, password = %s WHERE email = %s",
                (ADMIN_NAME, hash_password(ADMIN_PASS), ADMIN_EMAIL))
    conn.commit()
    print(f"✔ Usuario actualizado a admin: {ADMIN_EMAIL}")
else:
    cur.execute(
        "INSERT INTO users (name, email, password, role, balance) VALUES (%s, %s, %s, 'admin', 100)",
        (ADMIN_NAME, ADMIN_EMAIL, hash_password(ADMIN_PASS))
    )
    conn.commit()
    print(f"✔ Admin creado correctamente: {ADMIN_EMAIL}")

print(f"  Email:      {ADMIN_EMAIL}")
print(f"  Contraseña: {ADMIN_PASS}")
conn.close()
