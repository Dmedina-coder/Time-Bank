"""
Transaction Model
Modelo de datos para transacciones de tiempo
"""

from datetime import datetime

class Transaction:
    def __init__(self, id=None, from_user_id=None, to_user_id=None, 
                 amount=None, request_id=None, created_at=None):
        self.id = id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.amount = amount  # en horas
        self.request_id = request_id
        self.created_at = created_at or datetime.now()
        self.transaction_type = 'service_exchange'
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'from_user_id': self.from_user_id,
            'to_user_id': self.to_user_id,
            'amount': self.amount,
            'request_id': self.request_id,
            'created_at': self.created_at,
            'transaction_type': self.transaction_type
        }
