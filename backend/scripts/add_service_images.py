import os

import pymysql


def get_connection():
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', '127.0.0.1')
    db_port = int(os.getenv('DB_PORT', '3306'))
    db_name = os.getenv('DB_NAME')

    if not db_user or not db_password or not db_name:
        raise RuntimeError('Faltan variables de entorno DB_USER, DB_PASSWORD o DB_NAME')

    return pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
        charset='utf8mb4'
    )


def main():
    conn = get_connection()
    cur = conn.cursor()

    columns_to_add = [
        ('image_data', 'LONGBLOB DEFAULT NULL'),
        ('image_mime_type', 'VARCHAR(100) DEFAULT NULL'),
        ('image_filename', 'VARCHAR(255) DEFAULT NULL')
    ]

    added_any = False
    for column_name, column_definition in columns_to_add:
        cur.execute(
            "SELECT COUNT(*) FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'services' AND COLUMN_NAME = %s",
            (column_name,)
        )
        exists = cur.fetchone()[0]

        if not exists:
            cur.execute(f"ALTER TABLE services ADD COLUMN {column_name} {column_definition}")
            added_any = True
            print(f'OK: columna {column_name} añadida correctamente en services')
        else:
            print(f'INFO: la columna {column_name} ya existia en services')

    if added_any:
        conn.commit()

    conn.close()


if __name__ == '__main__':
    main()