"""
Review Model
Modelo de datos para reseñas
"""

from datetime import datetime

class Review:
    def __init__(self, id=None, request_id=None, reviewer_id=None, 
                 reviewed_user_id=None, rating=None, comment=None, created_at=None):
        self.id = id
        self.request_id = request_id
        self.reviewer_id = reviewer_id
        self.reviewed_user_id = reviewed_user_id
        self.rating = rating  # 1-5
        self.comment = comment
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'request_id': self.request_id,
            'reviewer_id': self.reviewer_id,
            'reviewed_user_id': self.reviewed_user_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at
        }
