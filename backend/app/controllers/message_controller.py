"""
Message Controller
Maneja la mensajería asociada a solicitudes
"""

from datetime import datetime

from flask import jsonify, request as flask_request
from sqlalchemy import text

from app import db


class MessageController:
    def __init__(self):
        pass

    def _current_user_id(self):
        if hasattr(flask_request, 'user'):
            return flask_request.user.get('user_id')
        return None

    def _is_admin(self):
        return hasattr(flask_request, 'user') and flask_request.user.get('role') == 'admin'

    def _get_request_access_row(self, request_id):
        return db.session.execute(
            text(
                """
                SELECT r.id, r.requester_id, r.provider_id, r.status,
                       s.title AS service_title,
                       rq.name AS requester_name,
                       pv.name AS provider_name
                FROM requests r
                LEFT JOIN services s ON r.service_id = s.id
                LEFT JOIN users rq ON r.requester_id = rq.id
                LEFT JOIN users pv ON r.provider_id = pv.id
                WHERE r.id = :request_id
                """
            ),
            {'request_id': request_id}
        ).mappings().first()

    def _ensure_access(self, request_row):
        if not request_row:
            return False, (jsonify({'error': 'Solicitud no encontrada'}), 404)

        current_user_id = self._current_user_id()
        if current_user_id and not self._is_admin():
            if int(request_row['requester_id']) != int(current_user_id) and int(request_row['provider_id']) != int(current_user_id):
                return False, (jsonify({'error': 'No autorizado para acceder a los mensajes de esta solicitud'}), 403)

        return True, None

    def _serialize_message_row(self, row):
        return {
            'id': row['id'],
            'request_id': row['request_id'],
            'sender_id': row['sender_id'],
            'sender_name': row.get('sender_name'),
            'content': row['content'],
            'read_at': row['read_at'].isoformat() if row.get('read_at') else None,
            'created_at': row['created_at'].isoformat() if row.get('created_at') else None
        }

    def get_request_messages(self, request_id):
        """Obtiene todos los mensajes de una solicitud"""
        try:
            request_row = self._get_request_access_row(request_id)
            allowed, response = self._ensure_access(request_row)
            if not allowed:
                return response

            page = max(int(flask_request.args.get('page', 1)), 1)
            per_page = min(max(int(flask_request.args.get('per_page', 50)), 1), 100)
            offset = (page - 1) * per_page

            total_row = db.session.execute(
                text("SELECT COUNT(*) AS total FROM request_messages WHERE request_id = :request_id"),
                {'request_id': request_id}
            ).mappings().first()

            rows = db.session.execute(
                text(
                    """
                    SELECT m.id, m.request_id, m.sender_id, u.name AS sender_name,
                           m.content, m.read_at, m.created_at
                    FROM request_messages m
                    LEFT JOIN users u ON m.sender_id = u.id
                    WHERE m.request_id = :request_id
                    ORDER BY m.created_at ASC, m.id ASC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                {'request_id': request_id, 'limit': per_page, 'offset': offset}
            ).mappings().all()

            return jsonify({
                'request': {
                    'id': request_row['id'],
                    'service_title': request_row.get('service_title'),
                    'requester_id': request_row['requester_id'],
                    'requester_name': request_row.get('requester_name'),
                    'provider_id': request_row['provider_id'],
                    'provider_name': request_row.get('provider_name'),
                    'status': request_row['status']
                },
                'items': [self._serialize_message_row(row) for row in rows],
                'total': int(total_row['total']) if total_row else 0,
                'page': page,
                'per_page': per_page
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo mensajes: {str(e)}'}), 500

    def create_request_message(self, request_id, data):
        """Crea un mensaje dentro de una solicitud"""
        try:
            data = data or {}
            content = str(data.get('content', '')).strip()

            if not content:
                return jsonify({'error': 'content es requerido'}), 400

            request_row = self._get_request_access_row(request_id)
            allowed, response = self._ensure_access(request_row)
            if not allowed:
                return response

            current_user_id = self._current_user_id()
            if not current_user_id:
                return jsonify({'error': 'Usuario no autenticado'}), 401

            if not self._is_admin():
                if int(request_row['requester_id']) != int(current_user_id) and int(request_row['provider_id']) != int(current_user_id):
                    return jsonify({'error': 'No autorizado para enviar mensajes en esta solicitud'}), 403

            result = db.session.execute(
                text(
                    """
                    INSERT INTO request_messages (request_id, sender_id, content, read_at)
                    VALUES (:request_id, :sender_id, :content, NULL)
                    """
                ),
                {
                    'request_id': request_id,
                    'sender_id': current_user_id,
                    'content': content
                }
            )
            message_id = result.lastrowid
            db.session.commit()

            row = db.session.execute(
                text(
                    """
                    SELECT m.id, m.request_id, m.sender_id, u.name AS sender_name,
                           m.content, m.read_at, m.created_at
                    FROM request_messages m
                    LEFT JOIN users u ON m.sender_id = u.id
                    WHERE m.id = :message_id
                    """
                ),
                {'message_id': message_id}
            ).mappings().first()

            return jsonify(self._serialize_message_row(row)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creando mensaje: {str(e)}'}), 500

    def mark_message_as_read(self, request_id, message_id):
        """Marca un mensaje de la solicitud como leído"""
        try:
            request_row = self._get_request_access_row(request_id)
            allowed, response = self._ensure_access(request_row)
            if not allowed:
                return response

            message_row = db.session.execute(
                text(
                    """
                    SELECT id, request_id, sender_id, read_at
                    FROM request_messages
                    WHERE id = :message_id AND request_id = :request_id
                    """
                ),
                {'message_id': message_id, 'request_id': request_id}
            ).mappings().first()

            if not message_row:
                return jsonify({'error': 'Mensaje no encontrado'}), 404

            current_user_id = self._current_user_id()
            if not current_user_id:
                return jsonify({'error': 'Usuario no autenticado'}), 401

            if not self._is_admin() and int(message_row['sender_id']) == int(current_user_id):
                return jsonify({'error': 'No puedes marcar como leído un mensaje que has enviado'}), 403

            if not self._is_admin() and int(request_row['requester_id']) != int(current_user_id) and int(request_row['provider_id']) != int(current_user_id):
                return jsonify({'error': 'No autorizado para marcar este mensaje como leído'}), 403

            if message_row.get('read_at'):
                return jsonify({'message': 'El mensaje ya estaba marcado como leído', 'message_id': message_id}), 200

            db.session.execute(
                text("UPDATE request_messages SET read_at = :read_at WHERE id = :message_id"),
                {'read_at': datetime.utcnow(), 'message_id': message_id}
            )
            db.session.commit()

            return jsonify({'message': 'Mensaje marcado como leído', 'message_id': message_id}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error marcando mensaje como leído: {str(e)}'}), 500

    def get_unread_count(self):
        """Devuelve el número de mensajes no leídos y los remitentes agrupados"""
        try:
            current_user_id = self._current_user_id()
            if not current_user_id:
                return jsonify({'error': 'Usuario no autenticado'}), 401

            # Total de mensajes no leídos
            total_row = db.session.execute(
                text(
                    """
                    SELECT COUNT(*) AS unread
                    FROM request_messages m
                    INNER JOIN requests r ON m.request_id = r.id
                    WHERE m.read_at IS NULL
                      AND m.sender_id != :user_id
                      AND (r.requester_id = :user_id OR r.provider_id = :user_id)
                    """
                ),
                {'user_id': current_user_id}
            ).mappings().first()

            # Detalle agrupado por remitente y solicitud
            sender_rows = db.session.execute(
                text(
                    """
                    SELECT u.name AS sender_name, r.id AS request_id,
                           COUNT(*) AS count
                    FROM request_messages m
                    INNER JOIN requests r ON m.request_id = r.id
                    INNER JOIN users u ON m.sender_id = u.id
                    WHERE m.read_at IS NULL
                      AND m.sender_id != :user_id
                      AND (r.requester_id = :user_id OR r.provider_id = :user_id)
                    GROUP BY m.sender_id, r.id, u.name
                    ORDER BY MAX(m.created_at) DESC
                    LIMIT 10
                    """
                ),
                {'user_id': current_user_id}
            ).mappings().all()

            # Solicitudes pendientes donde el usuario es proveedor (alguien solicitó su servicio)
            pending_rows = db.session.execute(
                text(
                    """
                    SELECT r.id AS request_id, s.title AS service_title,
                           u.name AS requester_name, r.created_at
                    FROM requests r
                    INNER JOIN services s ON r.service_id = s.id
                    INNER JOIN users u ON r.requester_id = u.id
                    WHERE r.provider_id = :user_id
                      AND r.status = 'pending'
                    ORDER BY r.created_at DESC
                    LIMIT 10
                    """
                ),
                {'user_id': current_user_id}
            ).mappings().all()

            return jsonify({
                'unread': int(total_row['unread']) if total_row else 0,
                'from': [
                    {
                        'name': row['sender_name'],
                        'request_id': row['request_id'],
                        'count': int(row['count'])
                    }
                    for row in sender_rows
                ],
                'pending_requests': [
                    {
                        'request_id': row['request_id'],
                        'service_title': row['service_title'],
                        'requester_name': row['requester_name']
                    }
                    for row in pending_rows
                ]
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo mensajes no leídos: {str(e)}'}), 500