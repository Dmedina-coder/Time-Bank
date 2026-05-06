"""
Message Model
Modelo de datos para mensajes asociados a solicitudes
"""

from datetime import datetime

from app import db


class RequestMessage(db.Model):
    __tablename__ = 'request_messages'

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id', ondelete='CASCADE'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    read_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'request_id': self.request_id,
            'sender_id': self.sender_id,
            'content': self.content,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }