"""
Notification Service
Lógica de negocio para envío de notificaciones
"""
from app.models import User
import logging

# Configura un logger para el servicio de notificaciones
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        pass
    
    def send_email(self, to_email, subject, body):
        """Envía un email. 
        NOTA: Esta es una implementación simulada. 
        En un entorno de producción, se integraría un servicio de correo real 
        (por ejemplo, usando Flask-Mail con SMTP, SendGrid, Mailgun, etc.).
        """
        logger.info(f"--- EMAIL SIMULADO ---")
        logger.info(f"Para: {to_email}")
        logger.info(f"Asunto: {subject}")
        logger.info(f"Cuerpo: {body}")
        logger.info(f"----------------------")
        # Aquí iría la lógica real de envío de email
        return True
    
    def send_request_notification(self, user_id, request_data):
        """Envía notificación de nueva solicitud"""
        user = User.query.get(user_id)
        if not user:
            return
        
        subject = "Nueva solicitud de servicio recibida"
        body = (
            f"Hola {user.name},\n\n"
            f"Has recibido una nueva solicitud para tu servicio '{request_data['service_title']}'.\n"
            f"Por favor, revisa la plataforma para aceptarla o rechazarla.\n\n"
            "Gracias,\nEl equipo de Time Bank"
        )
        self.send_email(user.email, subject, body)
    
    def send_acceptance_notification(self, user_id, request_id):
        """Envía notificación de solicitud aceptada"""
        user = User.query.get(user_id)
        if not user:
            return
            
        subject = "Tu solicitud de servicio ha sido aceptada"
        body = (
            f"Hola {user.name},\n\n"
            f"¡Buenas noticias! Tu solicitud de servicio (ID: {request_id}) ha sido aceptada.\n"
            "Puedes coordinar los detalles con el proveedor a través de la plataforma.\n\n"
            "Gracias,\nEl equipo de Time Bank"
        )
        self.send_email(user.email, subject, body)
    
    def send_completion_notification(self, user_id, request_id):
        """Envía notificación de servicio completado"""
        user = User.query.get(user_id)
        if not user:
            return

        subject = "Un servicio que solicitaste ha sido completado"
        body = (
            f"Hola {user.name},\n\n"
            f"El servicio asociado a tu solicitud (ID: {request_id}) ha sido marcado como completado por el proveedor.\n"
            "No olvides dejar una reseña sobre tu experiencia.\n\n"
            "Gracias,\nEl equipo de Time Bank"
        )
        self.send_email(user.email, subject, body)
    
    def send_credit_notification(self, user_id, transaction_data):
        """Envía notificación de cambio en créditos"""
        user = User.query.get(user_id)
        if not user:
            return

        credits = transaction_data.get('credits', 0)
        type_es = "recibido" if transaction_data.get('type') == 'credit' else "enviado"
        
        subject = f"Actualización de tu balance de créditos"
        body = (
            f"Hola {user.name},\n\n"
            f"Tu balance de créditos ha sido actualizado. Has {type_es} {credits} créditos.\n"
            f"Tu nuevo balance es: {user.balance} créditos.\n\n"
            "Gracias,\nEl equipo de Time Bank"
        )
        self.send_email(user.email, subject, body)
