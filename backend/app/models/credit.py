"""
Credit Model
Modelo de datos para créditos de tiempo
"""

from datetime import datetime

class Credit:
    def __init__(self, id=None, user_id=None, balance=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.balance = balance or 0  # en horas
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'updated_at': self.updated_at
        }
    
    def add_credits(self, amount):
        """Añade créditos"""
        self.balance += amount
        self.updated_at = datetime.now()
    
    def subtract_credits(self, amount):
        """Resta créditos"""
        if self.balance >= amount:
            self.balance -= amount
            self.updated_at = datetime.now()
            return True
        return False
