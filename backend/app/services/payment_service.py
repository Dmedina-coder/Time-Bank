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

    def _get_stripe_value(self, obj, key, default=None):
        if obj is None:
            return default

        if isinstance(obj, dict):
            return obj.get(key, default)

        try:
            return obj[key]
        except Exception:
            return getattr(obj, key, default)

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

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=selected_currency,
                payment_method_types=['card'],
                metadata={
                    'user_id': str(user_id),
                    'credits': str(credits)
                }
            )
        except stripe.error.StripeError as e:
            raise ValueError(f'Error creando PaymentIntent en Stripe: {str(e)}')

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

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        except stripe.error.InvalidRequestError:
            raise ValueError('PaymentIntent no encontrado en Stripe')
        except stripe.error.StripeError as e:
            raise ValueError(f'Error consultando Stripe: {str(e)}')

        if intent.status != 'succeeded':
            raise ValueError(f'El pago no está completado. Estado actual: {intent.status}')

        metadata = self._get_stripe_value(intent, 'metadata', None)
        metadata_user_id = self._get_stripe_value(metadata, 'user_id')
        if not metadata_user_id:
            raise ValueError('El pago no contiene información del usuario en metadata')
        
        if int(metadata_user_id) != int(user_id):
            raise ValueError('El pago no pertenece al usuario autenticado')

        credits_raw = self._get_stripe_value(metadata, 'credits')
        if not credits_raw:
            raise ValueError('El pago no contiene información de créditos en metadata')
        
        try:
            credits = int(credits_raw)
        except (TypeError, ValueError):
            raise ValueError(f'Cantidad de créditos inválida en metadata: {credits_raw}')

        if credits <= 0:
            raise ValueError('Cantidad de créditos debe ser mayor a 0')

        return {
            'payment_intent_id': intent.id,
            'amount_received': int(intent.amount_received or intent.amount),
            'currency': intent.currency,
            'credits': credits,
            'status': intent.status
        }
