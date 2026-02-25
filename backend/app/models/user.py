"""
User Model
Modelo de datos para usuarios
"""

from datetime import datetime

class User:
    def __init__(self, id=None, username=None, email=None, password_hash=None, 
                 full_name=None, phone=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.phone = phone
        self.created_at = created_at or datetime.now()
        self.is_active = True
        self.role = 'user'
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'created_at': self.created_at,
            'is_active': self.is_active,
            'role': self.role
        }
