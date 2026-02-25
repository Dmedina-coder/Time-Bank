"""
Request Model
Modelo de datos para solicitudes de servicios
"""

from datetime import datetime

class Request:
    def __init__(self, id=None, service_id=None, requester_id=None, 
                 provider_id=None, status=None, created_at=None):
        self.id = id
        self.service_id = service_id
        self.requester_id = requester_id
        self.provider_id = provider_id
        self.status = status or 'pending'  # pending, accepted, rejected, completed
        self.created_at = created_at or datetime.now()
        self.scheduled_date = None
        self.completed_date = None
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'service_id': self.service_id,
            'requester_id': self.requester_id,
            'provider_id': self.provider_id,
            'status': self.status,
            'created_at': self.created_at,
            'scheduled_date': self.scheduled_date,
            'completed_date': self.completed_date
        }
