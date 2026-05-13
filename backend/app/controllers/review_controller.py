"""
Review Controller
Maneja las peticiones relacionadas con valoraciones de servicios
"""

from flask import jsonify, request as flask_request
from sqlalchemy import text

from app import db


class ReviewController:
    def __init__(self):
        pass  # Sin dependencias adicionales

    def _is_admin(self):
        return hasattr(flask_request, 'user') and flask_request.user.get('role') == 'admin'

    def _current_user_id(self):
        if hasattr(flask_request, 'user'):
            return flask_request.user.get('user_id')
        return None

    def _serialize_review(self, row):
        return {
            'id': row['id'],
            'service_id': row['service_id'],
            'reviewer_id': row['reviewer_id'],
            'reviewer_name': row.get('reviewer_name'),
            'rating': row['rating'],
            'comment': row.get('comment'),
            'created_at': row['created_at'].isoformat() if row.get('created_at') else None
        }

    def get_service_reviews(self, service_id):
        """Obtiene todas las valoraciones de un servicio"""
        try:
            service = db.session.execute(
                text("SELECT id FROM services WHERE id = :sid AND status != 'deleted'"),
                {'sid': service_id}
            ).mappings().first()
            if not service:
                return jsonify({'error': 'Servicio no encontrado'}), 404

            rows = db.session.execute(
                text(
                    """
                    SELECT rv.id, rv.service_id, rv.reviewer_id, u.name AS reviewer_name,
                           rv.rating, rv.comment, rv.created_at
                    FROM reviews rv
                    LEFT JOIN users u ON rv.reviewer_id = u.id
                    WHERE rv.service_id = :service_id
                    ORDER BY rv.created_at DESC
                    """
                ),
                {'service_id': service_id}
            ).mappings().all()

            avg_row = db.session.execute(
                text("SELECT AVG(rating) AS avg_rating, COUNT(*) AS total FROM reviews WHERE service_id = :sid"),
                {'sid': service_id}
            ).mappings().first()

            return jsonify({
                'items': [self._serialize_review(r) for r in rows],
                'total': int(avg_row['total']) if avg_row else 0,
                'avg_rating': round(float(avg_row['avg_rating']), 1) if avg_row and avg_row['avg_rating'] else None
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo valoraciones: {str(e)}'}), 500

    def create_review(self, data):
        """Crea una valoración. Solo se permite si el usuario tiene una solicitud completada del servicio."""
        try:
            current_user_id = self._current_user_id()
            if not current_user_id:
                return jsonify({'error': 'No autenticado'}), 401

            data = data or {}
            service_id = data.get('service_id')
            rating_raw = data.get('rating')
            comment = (data.get('comment') or '').strip()

            if not service_id:
                return jsonify({'error': 'service_id es requerido'}), 400

            try:
                rating = int(rating_raw)
            except (TypeError, ValueError):
                return jsonify({'error': 'rating debe ser un entero entre 1 y 5'}), 400

            if rating < 1 or rating > 5:
                return jsonify({'error': 'rating debe estar entre 1 y 5'}), 400

            # Verificar que el servicio existe
            service = db.session.execute(
                text("SELECT id, owner_id FROM services WHERE id = :sid AND status != 'deleted'"),
                {'sid': service_id}
            ).mappings().first()
            if not service:
                return jsonify({'error': 'Servicio no encontrado'}), 404

            # El propietario no puede valorar su propio servicio
            if int(service['owner_id']) == int(current_user_id):
                return jsonify({'error': 'No puedes valorar tu propio servicio'}), 400

            # Verificar que el usuario tiene una solicitud completada de este servicio
            completed_request = db.session.execute(
                text(
                    """
                    SELECT id FROM requests
                    WHERE service_id = :service_id
                      AND requester_id = :reviewer_id
                      AND status = 'completed'
                    LIMIT 1
                    """
                ),
                {'service_id': service_id, 'reviewer_id': current_user_id}
            ).mappings().first()

            if not completed_request:
                return jsonify({'error': 'Solo puedes valorar servicios que hayas completado'}), 403

            # Verificar que no haya valorado ya este servicio
            existing = db.session.execute(
                text(
                    "SELECT id FROM reviews WHERE service_id = :sid AND reviewer_id = :rid LIMIT 1"
                ),
                {'sid': service_id, 'rid': current_user_id}
            ).mappings().first()

            if existing:
                return jsonify({'error': 'Ya has valorado este servicio'}), 409

            result = db.session.execute(
                text(
                    """
                    INSERT INTO reviews (service_id, reviewer_id, rating, comment)
                    VALUES (:service_id, :reviewer_id, :rating, :comment)
                    """
                ),
                {
                    'service_id': service_id,
                    'reviewer_id': current_user_id,
                    'rating': rating,
                    'comment': comment if comment else None
                }
            )
            review_id = result.lastrowid
            db.session.commit()

            row = db.session.execute(
                text(
                    """
                    SELECT rv.id, rv.service_id, rv.reviewer_id, u.name AS reviewer_name,
                           rv.rating, rv.comment, rv.created_at
                    FROM reviews rv
                    LEFT JOIN users u ON rv.reviewer_id = u.id
                    WHERE rv.id = :review_id
                    """
                ),
                {'review_id': review_id}
            ).mappings().first()

            return jsonify(self._serialize_review(row)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creando valoración: {str(e)}'}), 500

    def delete_review(self, review_id):
        """Elimina una valoración (solo admin)"""
        try:
            if not self._is_admin():
                return jsonify({'error': 'Acceso restringido a administradores'}), 403

            review = db.session.execute(
                text("SELECT id FROM reviews WHERE id = :rid"),
                {'rid': review_id}
            ).mappings().first()

            if not review:
                return jsonify({'error': 'Valoración no encontrada'}), 404

            db.session.execute(
                text("DELETE FROM reviews WHERE id = :rid"),
                {'rid': review_id}
            )
            db.session.commit()

            return jsonify({'message': 'Valoración eliminada correctamente'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error eliminando valoración: {str(e)}'}), 500
