"""
User Controller
Maneja las peticiones relacionadas con usuarios
"""
from flask import jsonify
from app.models.user import User
from app import db
from app.services.auth_service import AuthService

class UserController:
    def __init__(self):
        self.auth_service = AuthService()

    def get_current_user(self, request):
        """Obtiene el usuario autenticado actualmente"""
        user_id = request.user.get('user_id')
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(user.to_dict()), 200

    def update_current_user(self, request):
        """Actualiza el usuario autenticado actualmente"""
        user_id = request.user.get('user_id')
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            # Verificar si el nuevo email ya está en uso por otro usuario
            if data['email'] != user.email and User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'El email ya está en uso'}), 409
            user.email = data['email']
        if 'password' in data:
            if len(data['password']) < 8:
                return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres'}), 400
            user.password = self.auth_service.hash_password(data['password'])
        
        # Aquí se podría actualizar el perfil si existiera el modelo Profile
        # if 'profile' in data:
        #     ...

        db.session.commit()
        return jsonify(user.to_dict()), 200
    
    def get_user(self, user_id):
        """Obtiene información de un usuario por su ID"""
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(user.to_dict()), 200
    
    def update_user(self, user_id, data):
        """Actualiza información de un usuario (protegido, podría ser solo para admin)"""
        # Nota: Esta función debería estar protegida por el middleware de admin
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400

        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            if data['email'] != user.email and User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'El email ya está en uso'}), 409
            user.email = data['email']
        if 'role' in data:
            user.role = data['role']
        if 'balance' in data:
            user.balance = data['balance']

        db.session.commit()
        return jsonify(user.to_dict()), 200

