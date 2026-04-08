"""
Transaction Controller
Maneja las peticiones relacionadas con transacciones
"""

from flask import jsonify, request as flask_request
from sqlalchemy import text

from app import db
from app.models.user import User

class TransactionController:
    def __init__(self):
        pass

    def _serialize_transaction_row(self, row):
        return {
            'id': row['id'],
            'sender_id': row['sender_id'],
            'receiver_id': row['receiver_id'],
            'sender_name': row.get('sender_name'),
            'receiver_name': row.get('receiver_name'),
            'credits': row['credits'],
            'type': row['type'],
            'created_at': row['created_at'].isoformat() if row.get('created_at') else None
        }

    def _is_admin(self):
        return hasattr(flask_request, 'user') and flask_request.user.get('role') == 'admin'

    def _current_user_id(self):
        if hasattr(flask_request, 'user'):
            return flask_request.user.get('id')
        return None
    
    def get_transactions(self):
        """Obtiene lista de transacciones"""
        try:
            page = max(int(flask_request.args.get('page', 1)), 1)
            per_page = min(max(int(flask_request.args.get('per_page', 20)), 1), 100)
            offset = (page - 1) * per_page
            tx_type = flask_request.args.get('type')

            where_clauses = ["1=1"]
            params = {'limit': per_page, 'offset': offset}

            current_user_id = self._current_user_id()
            if current_user_id and not self._is_admin():
                where_clauses.append("(t.sender_id = :current_user_id OR t.receiver_id = :current_user_id)")
                params['current_user_id'] = current_user_id

            if tx_type:
                where_clauses.append("t.type = :tx_type")
                params['tx_type'] = tx_type

            where_sql = " AND ".join(where_clauses)

            total_row = db.session.execute(
                text(f"SELECT COUNT(*) AS total FROM transactions t WHERE {where_sql}"),
                params
            ).mappings().first()

            rows = db.session.execute(
                text(
                    f"""
                    SELECT t.id, t.sender_id, t.receiver_id, t.credits, t.type, t.created_at,
                           su.name AS sender_name, ru.name AS receiver_name
                    FROM transactions t
                    LEFT JOIN users su ON t.sender_id = su.id
                    LEFT JOIN users ru ON t.receiver_id = ru.id
                    WHERE {where_sql}
                    ORDER BY t.created_at DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                params
            ).mappings().all()

            response = {
                'items': [self._serialize_transaction_row(row) for row in rows],
                'total': int(total_row['total']) if total_row else 0,
                'page': page,
                'per_page': per_page
            }

            if current_user_id:
                user = User.query.get(current_user_id)
                response['balance'] = user.balance if user else 0

            return jsonify(response), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo transacciones: {str(e)}'}), 500
    
    def get_transaction(self, transaction_id):
        """Obtiene una transacción específica"""
        try:
            row = db.session.execute(
                text(
                    """
                    SELECT t.id, t.sender_id, t.receiver_id, t.credits, t.type, t.created_at,
                           su.name AS sender_name, ru.name AS receiver_name
                    FROM transactions t
                    LEFT JOIN users su ON t.sender_id = su.id
                    LEFT JOIN users ru ON t.receiver_id = ru.id
                    WHERE t.id = :transaction_id
                    """
                ),
                {'transaction_id': transaction_id}
            ).mappings().first()

            if not row:
                return jsonify({'error': 'Transacción no encontrada'}), 404

            current_user_id = self._current_user_id()
            if current_user_id and not self._is_admin():
                if row['sender_id'] != current_user_id and row['receiver_id'] != current_user_id:
                    return jsonify({'error': 'No autorizado para ver esta transacción'}), 403

            return jsonify(self._serialize_transaction_row(row)), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo transacción: {str(e)}'}), 500
    
    def create_transaction(self, data):
        """Crea una nueva transacción"""
        try:
            data = data or {}

            receiver_id = data.get('receiver_id')
            sender_id = self._current_user_id() or data.get('sender_id')
            tx_type = (data.get('type') or 'transfer').strip()

            try:
                credits = int(data.get('credits', 0))
            except (TypeError, ValueError):
                return jsonify({'error': 'credits debe ser un entero'}), 400

            if credits <= 0:
                return jsonify({'error': 'credits debe ser mayor a 0'}), 400

            allowed_types = {'transfer', 'purchase', 'refund', 'system'}
            if tx_type not in allowed_types:
                return jsonify({'error': 'type inválido'}), 400

            if receiver_id is not None:
                receiver = User.query.get(receiver_id)
                if not receiver:
                    return jsonify({'error': 'Usuario receptor no encontrado'}), 404
            else:
                receiver = None

            sender = User.query.get(sender_id) if sender_id is not None else None
            if sender_id is not None and not sender:
                return jsonify({'error': 'Usuario emisor no encontrado'}), 404

            if tx_type == 'transfer':
                if sender_id is None or receiver_id is None:
                    return jsonify({'error': 'transfer requiere sender_id y receiver_id'}), 400

                if int(sender_id) == int(receiver_id):
                    return jsonify({'error': 'No puedes transferirte créditos a ti mismo'}), 400

            if sender and sender.balance < credits:
                return jsonify({'error': 'Saldo insuficiente'}), 400

            if sender:
                sender.balance -= credits

            if receiver:
                receiver.balance += credits

            result = db.session.execute(
                text(
                    """
                    INSERT INTO transactions (sender_id, receiver_id, credits, type)
                    VALUES (:sender_id, :receiver_id, :credits, :tx_type)
                    """
                ),
                {
                    'sender_id': sender_id,
                    'receiver_id': receiver_id,
                    'credits': credits,
                    'tx_type': tx_type
                }
            )
            transaction_id = result.lastrowid
            db.session.commit()

            tx = db.session.execute(
                text(
                    """
                    SELECT t.id, t.sender_id, t.receiver_id, t.credits, t.type, t.created_at,
                           su.name AS sender_name, ru.name AS receiver_name
                    FROM transactions t
                    LEFT JOIN users su ON t.sender_id = su.id
                    LEFT JOIN users ru ON t.receiver_id = ru.id
                    WHERE t.id = :transaction_id
                    """
                ),
                {'transaction_id': transaction_id}
            ).mappings().first()

            return jsonify(self._serialize_transaction_row(tx)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creando transacción: {str(e)}'}), 500
    
    def get_user_transactions(self, user_id):
        """Obtiene transacciones de un usuario"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404

            current_user_id = self._current_user_id()
            if current_user_id and not self._is_admin() and int(current_user_id) != int(user_id):
                return jsonify({'error': 'No autorizado para ver estas transacciones'}), 403

            rows = db.session.execute(
                text(
                    """
                    SELECT t.id, t.sender_id, t.receiver_id, t.credits, t.type, t.created_at,
                           su.name AS sender_name, ru.name AS receiver_name
                    FROM transactions t
                    LEFT JOIN users su ON t.sender_id = su.id
                    LEFT JOIN users ru ON t.receiver_id = ru.id
                    WHERE t.sender_id = :user_id OR t.receiver_id = :user_id
                    ORDER BY t.created_at DESC
                    """
                ),
                {'user_id': user_id}
            ).mappings().all()

            return jsonify({
                'user_id': user_id,
                'balance': user.balance,
                'items': [self._serialize_transaction_row(row) for row in rows],
                'total': len(rows)
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo transacciones de usuario: {str(e)}'}), 500
