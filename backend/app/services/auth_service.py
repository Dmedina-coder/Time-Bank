"""
Auth Service
Lógica de negocio para autenticación
"""

import hashlib
import jwt
from datetime import datetime, timedelta

class AuthService:
    def __init__(self):
        self.secret_key = "your-secret-key-change-in-production"
    
    def hash_password(self, password):
        """Hashea una contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, password_hash):
        """Verifica una contraseña"""
        return self.hash_password(password) == password_hash
    
    def generate_token(self, user_id, username):
        """Genera un token JWT"""
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        """Verifica un token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
