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

    cur.execute(
        "SELECT COUNT(*) FROM information_schema.TABLES "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'request_messages'"
    )
    exists = cur.fetchone()[0]

    if not exists:
        cur.execute(
            """
            CREATE TABLE `request_messages` (
              `id` INT NOT NULL AUTO_INCREMENT,
              `request_id` INT NOT NULL,
              `sender_id` INT NOT NULL,
              `content` TEXT NOT NULL,
              `read_at` DATETIME DEFAULT NULL,
              `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (`id`),
              INDEX `idx_request_messages_request` (`request_id`),
              INDEX `idx_request_messages_sender` (`sender_id`),
              INDEX `idx_request_messages_created_at` (`created_at`),
              CONSTRAINT `fk_request_messages_request` FOREIGN KEY (`request_id`) REFERENCES `requests`(`id`) ON DELETE CASCADE ON UPDATE CASCADE,
              CONSTRAINT `fk_request_messages_sender` FOREIGN KEY (`sender_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        )
        conn.commit()
        print('OK: tabla request_messages creada correctamente')
    else:
        print('INFO: la tabla request_messages ya existia')

    conn.close()


if __name__ == '__main__':
    main()