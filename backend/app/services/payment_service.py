"""
Payment Service
Lógica de negocio para procesamiento de pagos en tiempo
"""
import os

import stripe

class PaymentService:
    def __init__(self):
        self.public_key = os.getenv('STRIPE_PUBLIC_KEY')
        self.private_key = os.getenv('STRIPE_PRIVATE_KEY')
        self.default_currency = (os.getenv('STRIPE_CURRENCY') or 'eur').lower()
        self.credit_price_cents = max(int(os.getenv('STRIPE_CREDIT_PRICE_CENTS', '100')), 1)

        if self.private_key:
            stripe.api_key = self.private_key

    def is_configured(self):
        return bool(self.private_key and self.public_key)

    def get_public_config(self):
        if not self.is_configured():
            raise ValueError('Stripe no está configurado correctamente en variables de entorno')

        return {
            'public_key': self.public_key,
            'currency': self.default_currency,
            'credit_price_cents': self.credit_price_cents
        }

    def create_payment_intent(self, user_id, credits, currency=None):
        if not self.is_configured():
            raise ValueError('Stripe no está configurado correctamente en variables de entorno')

        if credits <= 0:
            raise ValueError('credits debe ser mayor a 0')

        selected_currency = (currency or self.default_currency).lower()
        amount_cents = credits * self.credit_price_cents

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=selected_currency,
            automatic_payment_methods={'enabled': True},
            metadata={
                'user_id': str(user_id),
                'credits': str(credits)
            }
        )

        return {
            'payment_intent_id': intent.id,
            'client_secret': intent.client_secret,
            'amount': intent.amount,
            'currency': intent.currency,
            'credits': credits,
            'status': intent.status
        }

    def validate_successful_payment(self, payment_intent_id, user_id):
        if not self.is_configured():
            raise ValueError('Stripe no está configurado correctamente en variables de entorno')

        if not payment_intent_id:
            raise ValueError('payment_intent_id es requerido')

        intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if intent.status != 'succeeded':
            raise ValueError('El pago aún no está completado en Stripe')

        metadata_user_id = intent.metadata.get('user_id')
        if metadata_user_id and int(metadata_user_id) != int(user_id):
            raise ValueError('El pago no pertenece al usuario autenticado')

        credits_raw = intent.metadata.get('credits')
        try:
            credits = int(credits_raw)
        except (TypeError, ValueError):
            raise ValueError('No se pudo determinar la cantidad de créditos del pago')

        if credits <= 0:
            raise ValueError('Cantidad de créditos inválida en metadata de Stripe')

        return {
            'payment_intent_id': intent.id,
            'amount_received': intent.amount_received or intent.amount,
            'currency': intent.currency,
            'credits': credits,
            'status': intent.status
        }
