"""
Service Controller
Maneja las peticiones relacionadas con servicios
"""

from flask import jsonify, request as flask_request
from sqlalchemy import text

from app import db

class ServiceController:
    def __init__(self):
        pass

    def _serialize_service_row(self, row):
        return {
            'id': row['id'],
            'title': row['title'],
            'description': row['description'],
            'owner_id': row['owner_id'],
            'category': row['category'],
            'credits': row.get('credits', 1),
            'status': row['status'],
            'created_at': row['created_at'].isoformat() if row.get('created_at') else None,
            'owner_name': row.get('owner_name')
        }

    def _is_admin(self):
        return hasattr(flask_request, 'user') and flask_request.user.get('role') == 'admin'

    def _current_user_id(self):
        if hasattr(flask_request, 'user'):
            return flask_request.user.get('user_id')
        return None
    
    def get_services(self):
        """Obtiene lista de servicios"""
        try:
            page = max(int(flask_request.args.get('page', 1)), 1)
            per_page = min(max(int(flask_request.args.get('per_page', 20)), 1), 100)
            offset = (page - 1) * per_page

            category = flask_request.args.get('category')
            search = flask_request.args.get('search')
            status = flask_request.args.get('status')

            where_clauses = ["s.status != 'deleted'"]
            params = {'limit': per_page, 'offset': offset}

            if category:
                where_clauses.append("s.category = :category")
                params['category'] = category

            if search:
                where_clauses.append("(s.title LIKE :search OR s.description LIKE :search)")
                params['search'] = f"%{search}%"

            if status:
                where_clauses.append("s.status = :status")
                params['status'] = status

            where_sql = " AND ".join(where_clauses)

            total_row = db.session.execute(
                text(f"SELECT COUNT(*) AS total FROM services s WHERE {where_sql}"),
                params
            ).mappings().first()

            rows = db.session.execute(
                text(
                    f"""
                    SELECT s.id, s.title, s.description, s.owner_id, s.category, s.credits, s.status, s.created_at, u.name AS owner_name
                    FROM services s
                    LEFT JOIN users u ON s.owner_id = u.id
                    WHERE {where_sql}
                    ORDER BY s.created_at DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                params
            ).mappings().all()

            return jsonify({
                'items': [self._serialize_service_row(row) for row in rows],
                'total': int(total_row['total']) if total_row else 0,
                'page': page,
                'per_page': per_page
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo servicios: {str(e)}'}), 500
    
    def get_service(self, service_id):
        """Obtiene un servicio específico"""
        try:
            row = db.session.execute(
                text(
                    """
                    SELECT s.id, s.title, s.description, s.owner_id, s.category, s.credits, s.status, s.created_at,
                           u.name AS owner_name, u.email AS owner_email
                    FROM services s
                    LEFT JOIN users u ON s.owner_id = u.id
                    WHERE s.id = :service_id
                    """
                ),
                {'service_id': service_id}
            ).mappings().first()

            if not row or row['status'] == 'deleted':
                return jsonify({'error': 'Servicio no encontrado'}), 404

            return jsonify({
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'owner_id': row['owner_id'],
                'owner': {
                    'id': row['owner_id'],
                    'name': row.get('owner_name'),
                    'email': row.get('owner_email')
                },
                'category': row['category'],
                'credits': row.get('credits', 1),
                'status': row['status'],
                'created_at': row['created_at'].isoformat() if row.get('created_at') else None
            }), 200
        except Exception as e:
            return jsonify({'error': f'Error obteniendo servicio: {str(e)}'}), 500
    
    def create_service(self, data):
        """Crea un nuevo servicio"""
        try:
            data = data or {}

            title = (data.get('title') or '').strip()
            description = (data.get('description') or '').strip()
            category = (data.get('category') or '').strip()

            try:
                credits = max(int(data.get('credits', 1)), 1)
            except (TypeError, ValueError):
                credits = 1

            owner_id = self._current_user_id() or data.get('owner_id')

            if not title or not description or not category:
                return jsonify({'error': 'title, description y category son requeridos'}), 400

            if not owner_id:
                return jsonify({'error': 'owner_id es requerido'}), 400

            result = db.session.execute(
                text(
                    """
                    INSERT INTO services (title, description, owner_id, category, credits, status)
                    VALUES (:title, :description, :owner_id, :category, :credits, 'active')
                    """
                ),
                {
                    'title': title,
                    'description': description,
                    'owner_id': owner_id,
                    'category': category,
                    'credits': credits
                }
            )
            service_id = result.lastrowid
            db.session.commit()

            service = db.session.execute(
                text(
                    """
                    SELECT s.id, s.title, s.description, s.owner_id, s.category, s.credits, s.status, s.created_at,
                           u.name AS owner_name
                    FROM services s
                    LEFT JOIN users u ON s.owner_id = u.id
                    WHERE s.id = :service_id
                    """
                ),
                {'service_id': service_id}
            ).mappings().first()

            return jsonify(self._serialize_service_row(service)), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error creando servicio: {str(e)}'}), 500
    
    def update_service(self, service_id, data):
        """Actualiza un servicio"""
        try:
            data = data or {}

            service = db.session.execute(
                text("SELECT id, owner_id, status FROM services WHERE id = :service_id"),
                {'service_id': service_id}
            ).mappings().first()

            if not service or service['status'] == 'deleted':
                return jsonify({'error': 'Servicio no encontrado'}), 404

            current_user_id = self._current_user_id()
            if current_user_id and not self._is_admin() and int(service['owner_id']) != int(current_user_id):
                return jsonify({'error': 'No autorizado para actualizar este servicio'}), 403

            allowed_status = {'active', 'inactive', 'deleted'}
            fields = {}

            if 'title' in data and data['title'] is not None:
                title = str(data['title']).strip()
                if not title:
                    return jsonify({'error': 'title no puede estar vacío'}), 400
                fields['title'] = title

            if 'description' in data and data['description'] is not None:
                description = str(data['description']).strip()
                if not description:
                    return jsonify({'error': 'description no puede estar vacío'}), 400
                fields['description'] = description

            if 'category' in data and data['category'] is not None:
                category = str(data['category']).strip()
                if not category:
                    return jsonify({'error': 'category no puede estar vacío'}), 400
                fields['category'] = category

            if 'status' in data and data['status'] is not None:
                status = str(data['status']).strip()
                if status not in allowed_status:
                    return jsonify({'error': 'status inválido'}), 400
                fields['status'] = status

            if 'credits' in data and data['credits'] is not None:
                try:
                    credits_val = max(int(data['credits']), 1)
                    fields['credits'] = credits_val
                except (TypeError, ValueError):
                    return jsonify({'error': 'credits debe ser un entero positivo'}), 400

            if not fields:
                return jsonify({'error': 'No hay campos válidos para actualizar'}), 400

            set_clause = ', '.join([f"{key} = :{key}" for key in fields.keys()])
            fields['service_id'] = service_id

            db.session.execute(
                text(f"UPDATE services SET {set_clause} WHERE id = :service_id"),
                fields
            )
            db.session.commit()

            updated = db.session.execute(
                text(
                    """
                    SELECT s.id, s.title, s.description, s.owner_id, s.category, s.credits, s.status, s.created_at,
                           u.name AS owner_name
                    FROM services s
                    LEFT JOIN users u ON s.owner_id = u.id
                    WHERE s.id = :service_id
                    """
                ),
                {'service_id': service_id}
            ).mappings().first()

            return jsonify(self._serialize_service_row(updated)), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error actualizando servicio: {str(e)}'}), 500
    
    def delete_service(self, service_id):
        """Elimina un servicio"""
        try:
            service = db.session.execute(
                text("SELECT id, owner_id, status FROM services WHERE id = :service_id"),
                {'service_id': service_id}
            ).mappings().first()

            if not service or service['status'] == 'deleted':
                return jsonify({'error': 'Servicio no encontrado'}), 404

            current_user_id = self._current_user_id()
            if current_user_id and not self._is_admin() and int(service['owner_id']) != int(current_user_id):
                return jsonify({'error': 'No autorizado para eliminar este servicio'}), 403

            db.session.execute(
                text("UPDATE services SET status = 'deleted' WHERE id = :service_id"),
                {'service_id': service_id}
            )
            db.session.commit()

            return jsonify({'message': 'Servicio eliminado correctamente'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error eliminando servicio: {str(e)}'}), 500
