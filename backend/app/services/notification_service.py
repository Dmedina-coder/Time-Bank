"""
Notification Service
Lógica de negocio para envío de notificaciones
"""

class NotificationService:
    def __init__(self):
        pass
    
    def send_email(self, to_email, subject, body):
        """Envía un email"""
        pass
    
    def send_request_notification(self, user_id, request_data):
        """Envía notificación de nueva solicitud"""
        pass
    
    def send_acceptance_notification(self, user_id, request_id):
        """Envía notificación de solicitud aceptada"""
        pass
    
    def send_completion_notification(self, user_id, request_id):
        """Envía notificación de servicio completado"""
        pass
    
    def send_credit_notification(self, user_id, transaction_data):
        """Envía notificación de cambio en créditos"""
        pass
