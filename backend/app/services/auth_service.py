"""
Auth Service
Lógica de negocio para autenticación
"""

import hashlib
import jwt
from datetime import datetime, timedelta
from flask import current_app

class AuthService:
    def __init__(self):
        # No inicializar con current_app aquí
        pass
    
    def _get_secret_key(self):
        return current_app.config['JWT_SECRET_KEY']

    def _get_salt(self):
        return current_app.config['PASSWORD_HASH_SALT']

    def hash_password(self, password):
        """Hashea una contraseña con salt"""
        salted_password = self._get_salt() + password
        return hashlib.sha256(salted_password.encode()).hexdigest()
    
    def verify_password(self, password, password_hash):
        """Verifica una contraseña hasheada con salt"""
        return self.hash_password(password) == password_hash
    
    def generate_token(self, user_id, role):
        """Genera un token JWT"""
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self._get_secret_key(), algorithm='HS256')
    
    def verify_token(self, token):
        """Verifica un token JWT"""
        try:
            payload = jwt.decode(token, self._get_secret_key(), algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
