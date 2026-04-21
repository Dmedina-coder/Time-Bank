"""
Auth Controller
Maneja las peticiones relacionadas con autenticación
"""
from flask import jsonify
from app.services.auth_service import AuthService
from app.models.user import User
from app import db

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
    
    def login(self, request):
        """Maneja el inicio de sesión"""
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user or not self.auth_service.verify_password(data['password'], user.password):
            return jsonify({'error': 'Credenciales inválidas'}), 401

        access_token = self.auth_service.generate_token(user.id, user.role)
        
        return jsonify({
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 86400, # 1 día en segundos
            'user': user.to_dict()
        }), 200
    
    def register(self, request):
        """Maneja el registro de usuarios"""
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({'error': 'Nombre, email y contraseña son requeridos'}), 400

        if len(data['password']) < 8:
            return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'El email ya está en uso'}), 409

        hashed_password = self.auth_service.hash_password(data['password'])
        
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            role=data.get('role', 'user')
        )
        
        db.session.add(new_user)
        db.session.commit()

        access_token = self.auth_service.generate_token(new_user.id, new_user.role)

        return jsonify({
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 86400,
            'user': new_user.to_dict()
        }), 201
    
    def logout(self, request):
        """Maneja el cierre de sesión"""
        # Para JWT, el logout es manejado por el cliente al destruir el token.
        # Se puede implementar una blocklist de tokens si se necesita.
        return jsonify({'message': 'Logout exitoso'}), 204

