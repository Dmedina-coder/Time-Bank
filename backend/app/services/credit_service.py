"""
Credit Service
Lógica de negocio para gestión de créditos
"""
from app.models import User, Transaction
from app import db

class CreditService:
    def __init__(self):
        pass
    
    def get_credit_balance(self, user_id):
        """Obtiene el balance de créditos de un usuario"""
        user = User.query.get(user_id)
        return user.balance if user else 0
    
    def add_credits(self, user_id, amount, reason):
        """Añade créditos a un usuario"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        user.balance += amount
        transaction = Transaction(
            receiver_id=user_id,
            credits=amount,
            type='credit',
            reason=reason
        )
        db.session.add(transaction)
        db.session.commit()
        return user.balance
    
    def deduct_credits(self, user_id, amount, reason):
        """Deduce créditos de un usuario"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        if user.balance < amount:
            raise ValueError("Insufficient credits")
            
        user.balance -= amount
        transaction = Transaction(
            sender_id=user_id,
            credits=amount,
            type='debit',
            reason=reason
        )
        db.session.add(transaction)
        db.session.commit()
        return user.balance
    
    def get_credit_history(self, user_id):
        """Obtiene el historial de créditos de un usuario"""
        return Transaction.query.filter(
            (Transaction.sender_id == user_id) | (Transaction.receiver_id == user_id)
        ).order_by(Transaction.created_at.desc()).all()
    
    def transfer_credits(self, from_user_id, to_user_id, amount):
        """Transfiere créditos entre usuarios"""
        from_user = User.query.get(from_user_id)
        to_user = User.query.get(to_user_id)

        if not from_user or not to_user:
            raise ValueError("User not found")

        if from_user.balance < amount:
            raise ValueError("Insufficient credits")

        from_user.balance -= amount
        to_user.balance += amount

        transaction = Transaction(
            sender_id=from_user_id,
            receiver_id=to_user_id,
            credits=amount,
            type='transfer'
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction
