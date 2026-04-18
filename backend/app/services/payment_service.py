"""
Payment Service
Lógica de negocio para procesamiento de pagos en tiempo
"""
from .credit_service import CreditService

class PaymentService:
    def __init__(self):
        self.credit_service = CreditService()
    
    def process_time_transfer(self, from_user_id, to_user_id, hours):
        """Procesa una transferencia de tiempo entre usuarios"""
        # Verificar saldo suficiente
        if not self.validate_balance(from_user_id, hours):
            raise ValueError("Insufficient balance to make the transfer.")
        
        # Realizar transferencia y registrar transacción
        try:
            transaction = self.credit_service.transfer_credits(from_user_id, to_user_id, hours)
            return transaction
        except ValueError as e:
            # Re-lanzar la excepción para que sea manejada en una capa superior
            raise e
    
    def validate_balance(self, user_id, required_hours):
        """Valida si un usuario tiene suficiente saldo"""
        current_balance = self.get_user_balance(user_id)
        return current_balance >= required_hours
    
    def get_user_balance(self, user_id):
        """Obtiene el saldo de un usuario"""
        return self.credit_service.get_credit_balance(user_id)
    
    def add_initial_credits(self, user_id, hours):
        """Añade créditos iniciales a un nuevo usuario"""
        try:
            self.credit_service.add_credits(user_id, hours, reason="Initial credits for new user")
            return True
        except ValueError:
            return False
