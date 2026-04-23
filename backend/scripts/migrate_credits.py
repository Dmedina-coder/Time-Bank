import pymysql

conn = pymysql.connect(
    host='dmedinaserver.duckdns.org',
    port=3306,
    user='TimeUser',
    password='Tb2026-K9f8_rX',
    database='timebank',
    charset='utf8mb4'
)
cur = conn.cursor()

cur.execute(
    "SELECT COUNT(*) FROM information_schema.COLUMNS "
    "WHERE TABLE_SCHEMA='timebank' AND TABLE_NAME='services' AND COLUMN_NAME='credits'"
)
exists = cur.fetchone()[0]

if not exists:
    cur.execute('ALTER TABLE services ADD COLUMN credits INT NOT NULL DEFAULT 1')
    conn.commit()
    print('OK: columna credits añadida correctamente')
else:
    print('INFO: la columna credits ya existia')

conn.close()
