"""
Admin Controller
Maneja las peticiones administrativas
"""

from flask import jsonify
from sqlalchemy import text

from app import db
from app.models.user import User

class AdminController:
    def __init__(self):
        pass
    
    def get_stats(self):
        """Obtiene estadísticas del sistema"""
        try:
            total_users = User.query.count()
            total_admins = User.query.filter_by(role='admin').count()

            service_rows = db.session.execute(
                text(
                    """
                    SELECT status, COUNT(*) AS total
                    FROM services
                    GROUP BY status
                    """
                )
            ).mappings().all()

            request_rows = db.session.execute(
                text(
                    """
                    SELECT status, COUNT(*) AS total
                    FROM requests
                    GROUP BY status
                    """
                )
            ).mappings().all()

            transaction_summary = db.session.execute(
                text(
                    """
                    SELECT COUNT(*) AS total_transactions, COALESCE(SUM(credits), 0) AS total_credits
                    FROM transactions
                    """
                )
            ).mappings().first()

            services_by_status = {row['status']: int(row['total']) for row in service_rows}
            requests_by_status = {row['status']: int(row['total']) for row in request_rows}

            return jsonify({
                'users': {
                    'total': total_users,
                    'admins': total_admins
                },
                'services': {
                    'by_status': services_by_status
                },
                'requests': {
                    'by_status': requests_by_status
                },
                'transactions': {
                    'total': int(transaction_summary['total_transactions']) if transaction_summary else 0,
                    'credits_sum': int(transaction_summary['total_credits']) if transaction_summary else 0
                }
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo estadísticas: {str(e)}'}), 500
    
    def get_all_users(self, request=None):
        """Obtiene todos los usuarios"""
        try:
            query = User.query

            if request is not None:
                search = request.args.get('search', '').strip()
                if search:
                    search_filter = f"%{search}%"
                    query = query.filter(
                        (User.name.ilike(search_filter)) |
                        (User.email.ilike(search_filter))
                    )

            users = query.order_by(User.created_at.desc()).all()
            return jsonify([user.to_dict() for user in users]), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo usuarios: {str(e)}'}), 500
    
    def approve_service(self, service_id):
        """Aprueba un servicio"""
        try:
            service = db.session.execute(
                text("SELECT id, status FROM services WHERE id = :service_id"),
                {'service_id': service_id}
            ).mappings().first()

            if not service:
                return jsonify({'error': 'Servicio no encontrado'}), 404

            db.session.execute(
                text("UPDATE services SET status = 'active' WHERE id = :service_id"),
                {'service_id': service_id}
            )
            db.session.commit()

            return jsonify({
                'message': 'Servicio aprobado correctamente',
                'service_id': service_id,
                'status': 'active'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error aprobando servicio: {str(e)}'}), 500
    
    def reject_service(self, service_id):
        """Rechaza un servicio"""
        try:
            service = db.session.execute(
                text("SELECT id, status FROM services WHERE id = :service_id"),
                {'service_id': service_id}
            ).mappings().first()

            if not service:
                return jsonify({'error': 'Servicio no encontrado'}), 404

            db.session.execute(
                text("UPDATE services SET status = 'inactive' WHERE id = :service_id"),
                {'service_id': service_id}
            )
            db.session.commit()

            return jsonify({
                'message': 'Servicio rechazado correctamente',
                'service_id': service_id,
                'status': 'inactive'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error rechazando servicio: {str(e)}'}), 500
    
    def manage_credits(self, user_id, amount):
        """Gestiona créditos de usuario"""
        try:
            try:
                amount = int(amount)
            except (TypeError, ValueError):
                return jsonify({'error': 'El monto debe ser un entero'}), 400

            if amount == 0:
                return jsonify({'error': 'El monto no puede ser 0'}), 400

            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 404

            new_balance = user.balance + amount
            if new_balance < 0:
                return jsonify({'error': 'Saldo insuficiente para realizar el ajuste'}), 400

            user.balance = new_balance

            db.session.execute(
                text(
                    """
                    INSERT INTO transactions (sender_id, receiver_id, credits, type)
                    VALUES (:sender_id, :receiver_id, :credits, :type)
                    """
                ),
                {
                    'sender_id': None,
                    'receiver_id': user.id,
                    'credits': amount,
                    'type': 'system'
                }
            )

            db.session.commit()

            return jsonify({
                'message': 'Créditos ajustados correctamente',
                'user': user.to_dict(),
                'adjustment': amount,
                'new_balance': user.balance
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error gestionando créditos: {str(e)}'}), 500
