"""
Service Model
Modelo de datos para servicios
"""

from datetime import datetime

class Service:
    def __init__(self, id=None, title=None, description=None, category=None,
                 duration=None, user_id=None, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.duration = duration  # en horas
        self.user_id = user_id
        self.created_at = created_at or datetime.now()
        self.status = 'active'
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'duration': self.duration,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'status': self.status
        }
