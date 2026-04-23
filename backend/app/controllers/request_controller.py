"""
Request Controller
Maneja las peticiones relacionadas con solicitudes de servicios
"""

from datetime import datetime

from flask import jsonify, request as flask_request
from sqlalchemy import text

from app import db
from app.models.user import User


class RequestController:
    def __init__(self):
        pass

    def _serialize_request_row(self, row):
        return {
            'id': row['id'],
            'service_id': row['service_id'],
            'service_title': row.get('service_title'),
            'requester_id': row['requester_id'],
            'requester_name': row.get('requester_name'),
            'provider_id': row['provider_id'],
            'provider_name': row.get('provider_name'),
            'status': row['status'],
            'scheduled_date': row['scheduled_date'].isoformat() if row.get('scheduled_date') else None,
            'created_at': row['created_at'].isoformat() if row.get('created_at') else None
        }

    def _is_admin(self):
        return hasattr(flask_request, 'user') and flask_request.user.get('role') == 'admin'

    def _current_user_id(self):
        if hasattr(flask_request, 'user'):
            return flask_request.user.get('user_id')
        return None

    def _parse_datetime(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if not isinstance(value, str):
            return None

        normalized = value.strip().replace('Z', '+00:00')
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            return None

    def get_requests(self):
        """Obtiene lista de solicitudes"""
        try:
            page = max(int(flask_request.args.get('page', 1)), 1)
            per_page = min(max(int(flask_request.args.get('per_page', 20)), 1), 100)
            offset = (page - 1) * per_page

            status = flask_request.args.get('status')
            service_id = flask_request.args.get('service_id')

            where_clauses = ["1=1"]
            params = {'limit': per_page, 'offset': offset}

            current_user_id = self._current_user_id()
            if current_user_id and not self._is_admin():
                where_clauses.append("(r.requester_id = :current_user_id OR r.provider_id = :current_user_id)")
                params['current_user_id'] = current_user_id

            if status:
                where_clauses.append("r.status = :status")
                params['status'] = status

            if service_id:
                where_clauses.append("r.service_id = :service_id")
                params['service_id'] = service_id

            where_sql = " AND ".join(where_clauses)

            total_row = db.session.execute(
                text(f"SELECT COUNT(*) AS total FROM requests r WHERE {where_sql}"),
                params
            ).mappings().first()

            rows = db.session.execute(
                text(
                    f"""
                    SELECT r.id, r.service_id, s.title AS service_title,
                           r.requester_id, rq.name AS requester_name,
                           r.provider_id, pv.name AS provider_name,
                           r.status, r.scheduled_date, r.created_at
                    FROM requests r
                    LEFT JOIN services s ON r.service_id = s.id
                    LEFT JOIN users rq ON r.requester_id = rq.id
                    LEFT JOIN users pv ON r.provider_id = pv.id
                    WHERE {where_sql}
                    ORDER BY r.created_at DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                params
            ).mappings().all()

            return jsonify({
                'items': [self._serialize_request_row(row) for row in rows],
                'total': int(total_row['total']) if total_row else 0,
                'page': page,
                'per_page': per_page
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo solicitudes: {str(e)}'}), 500

    def get_request(self, request_id):
        """Obtiene una solicitud específica"""
        try:
            row = db.session.execute(
                text(
                    """
                    SELECT r.id, r.service_id, s.title AS service_title,
                           r.requester_id, rq.name AS requester_name,
                           r.provider_id, pv.name AS provider_name,
                           r.status, r.scheduled_date, r.created_at
                    FROM requests r
                    LEFT JOIN services s ON r.service_id = s.id
                    LEFT JOIN users rq ON r.requester_id = rq.id
                    LEFT JOIN users pv ON r.provider_id = pv.id
                    WHERE r.id = :request_id
                    """
                ),
                {'request_id': request_id}
            ).mappings().first()

            if not row:
                return jsonify({'error': 'Solicitud no encontrada'}), 404

            current_user_id = self._current_user_id()
            if current_user_id and not self._is_admin():
                if row['requester_id'] != current_user_id and row['provider_id'] != current_user_id:
                    return jsonify({'error': 'No autorizado para ver esta solicitud'}), 403

            return jsonify(self._serialize_request_row(row)), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo solicitud: {str(e)}'}), 500

    def create_request(self, data):
        """Crea una nueva solicitud"""
        try:
            data = data or {}
            requester_id = self._current_user_id() or data.get('requester_id')
            service_id = data.get('service_id')
            scheduled_date_raw = data.get('scheduled_date')

            if not requester_id or not service_id:
                return jsonify({'error': 'requester_id y service_id son requeridos'}), 400

            scheduled_date = self._parse_datetime(scheduled_date_raw)
            if not scheduled_date:
                return jsonify({'error': 'scheduled_date inválido. Usa formato ISO 8601'}), 400

            service = db.session.execute(
                text("SELECT id, owner_id, status FROM services WHERE id = :service_id"),
                {'service_id': service_id}
            ).mappings().first()

            if not service or service['status'] != 'active':
                return jsonify({'error': 'Servicio no disponible para solicitar'}), 404

            if int(service['owner_id']) == int(requester_id):
                return jsonify({'error': 'No puedes solicitar tu propio servicio'}), 400

            result = db.session.execute(
                text(
                    """
                    INSERT INTO requests (service_id, requester_id, provider_id, status, scheduled_date)
                    VALUES (:service_id, :requester_id, :provider_id, 'pending', :scheduled_date)
                    """
                ),
                {
                    'service_id': service_id,
                    'requester_id': requester_id,
                    'provider_id': service['owner_id'],
                    'scheduled_date': scheduled_date
                }
            )
            new_request_id = result.lastrowid
            db.session.commit()

            row = db.session.execute(
                text(
                    """
                    SELECT r.id, r.service_id, s.title AS service_title,
                           r.requester_id, rq.name AS requester_name,
                           r.provider_id, pv.name AS provider_name,
                           r.status, r.scheduled_date, r.created_at
                    FROM requests r
                    LEFT JOIN services s ON r.service_id = s.id
                    LEFT JOIN users rq ON r.requester_id = rq.id
                    LEFT JOIN users pv ON r.provider_id = pv.id
                    WHERE r.id = :request_id
                    """
                ),
                {'request_id': new_request_id}
            ).mappings().first()

            return jsonify(self._serialize_request_row(row)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creando solicitud: {str(e)}'}), 500

    def update_request(self, request_id, data):
        """Actualiza una solicitud"""
        try:
            data = data or {}

            current = db.session.execute(
                text(
                    """
                    SELECT id, requester_id, provider_id, status, scheduled_date
                    FROM requests
                    WHERE id = :request_id
                    """
                ),
                {'request_id': request_id}
            ).mappings().first()

            if not current:
                return jsonify({'error': 'Solicitud no encontrada'}), 404

            current_user_id = self._current_user_id()
            is_admin = self._is_admin()
            if current_user_id and not is_admin:
                if int(current['requester_id']) != int(current_user_id) and int(current['provider_id']) != int(current_user_id):
                    return jsonify({'error': 'No autorizado para actualizar esta solicitud'}), 403

            allowed_status = {'pending', 'accepted', 'rejected', 'completed', 'cancelled'}
            updates = {}

            if 'scheduled_date' in data and data['scheduled_date'] is not None:
                scheduled_date = self._parse_datetime(data['scheduled_date'])
                if not scheduled_date:
                    return jsonify({'error': 'scheduled_date inválido. Usa formato ISO 8601'}), 400
                updates['scheduled_date'] = scheduled_date

            if 'status' in data and data['status'] is not None:
                next_status = str(data['status']).strip()
                if next_status not in allowed_status:
                    return jsonify({'error': 'status inválido'}), 400

                if not is_admin and current_user_id:
                    if next_status in {'accepted', 'rejected', 'completed'} and int(current['provider_id']) != int(current_user_id):
                        return jsonify({'error': 'Solo el proveedor puede cambiar a ese estado'}), 403
                    if next_status == 'cancelled' and int(current['provider_id']) != int(current_user_id) and int(current['requester_id']) != int(current_user_id):
                        return jsonify({'error': 'Solo requester o provider pueden cancelar'}), 403

                updates['status'] = next_status

            if not updates:
                return jsonify({'error': 'No hay campos válidos para actualizar'}), 400

            set_clause = ', '.join([f"{field} = :{field}" for field in updates.keys()])
            updates['request_id'] = request_id

            db.session.execute(
                text(f"UPDATE requests SET {set_clause} WHERE id = :request_id"),
                updates
            )

            # Transferencia automática de créditos al completar el servicio
            if updates.get('status') == 'completed' and current['status'] not in ('completed', 'cancelled', 'rejected'):
                service_row = db.session.execute(
                    text("""
                        SELECT s.credits
                        FROM requests r
                        JOIN services s ON r.service_id = s.id
                        WHERE r.id = :request_id
                    """),
                    {'request_id': request_id}
                ).mappings().first()

                requester = User.query.get(int(current['requester_id']))
                provider = User.query.get(int(current['provider_id']))

                if not requester or not provider:
                    db.session.rollback()
                    return jsonify({'error': 'No se encontraron usuarios para la transacción'}), 400

                service_credits = int(service_row['credits']) if service_row and service_row.get('credits') else 1

                if requester.balance < service_credits:
                    db.session.rollback()
                    return jsonify({'error': f'Saldo insuficiente. Se requieren {service_credits} créditos para completar el servicio'}), 400

                requester.balance -= service_credits
                provider.balance += service_credits

                db.session.execute(
                    text("""
                        INSERT INTO transactions (sender_id, receiver_id, credits, type)
                        VALUES (:sender_id, :receiver_id, :credits, 'purchase')
                    """),
                    {
                        'sender_id': requester.id,
                        'receiver_id': provider.id,
                        'credits': service_credits
                    }
                )

            db.session.commit()

            row = db.session.execute(
                text(
                    """
                    SELECT r.id, r.service_id, s.title AS service_title,
                           r.requester_id, rq.name AS requester_name,
                           r.provider_id, pv.name AS provider_name,
                           r.status, r.scheduled_date, r.created_at
                    FROM requests r
                    LEFT JOIN services s ON r.service_id = s.id
                    LEFT JOIN users rq ON r.requester_id = rq.id
                    LEFT JOIN users pv ON r.provider_id = pv.id
                    WHERE r.id = :request_id
                    """
                ),
                {'request_id': request_id}
            ).mappings().first()

            return jsonify(self._serialize_request_row(row)), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error actualizando solicitud: {str(e)}'}), 500

    def cancel_request(self, request_id):
        """Cancela una solicitud"""
        try:
            current = db.session.execute(
                text(
                    """
                    SELECT id, requester_id, provider_id, status
                    FROM requests
                    WHERE id = :request_id
                    """
                ),
                {'request_id': request_id}
            ).mappings().first()

            if not current:
                return jsonify({'error': 'Solicitud no encontrada'}), 404

            if current['status'] in {'completed', 'cancelled', 'rejected'}:
                return jsonify({'error': f'No se puede cancelar una solicitud en estado {current["status"]}'}), 400

            current_user_id = self._current_user_id()
            is_admin = self._is_admin()
            if current_user_id and not is_admin:
                if int(current['requester_id']) != int(current_user_id) and int(current['provider_id']) != int(current_user_id):
                    return jsonify({'error': 'No autorizado para cancelar esta solicitud'}), 403

            db.session.execute(
                text("UPDATE requests SET status = 'cancelled' WHERE id = :request_id"),
                {'request_id': request_id}
            )
            db.session.commit()

            return jsonify({'message': 'Solicitud cancelada correctamente', 'request_id': request_id, 'status': 'cancelled'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error cancelando solicitud: {str(e)}'}), 500
