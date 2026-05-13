"""
API Routes
Define todas las rutas de la API
"""

from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.controllers.admin_controller import AdminController
from app.controllers.service_controller import ServiceController
from app.controllers.request_controller import RequestController
from app.controllers.message_controller import MessageController
from app.controllers.transaction_controller import TransactionController
from app.controllers.review_controller import ReviewController
from app.middleware.auth_middleware import AuthMiddleware
from app.services.auth_service import AuthService

api = Blueprint('api', __name__)

# Instanciar servicios y middleware
auth_service = AuthService()
auth_middleware = AuthMiddleware(auth_service)

# Instanciar controladores
auth_controller = AuthController()
user_controller = UserController()
admin_controller = AdminController()
service_controller = ServiceController()
request_controller = RequestController()
message_controller = MessageController()
transaction_controller = TransactionController()
review_controller = ReviewController()

# Rutas de autenticación
@api.route('/auth/login', methods=['POST'])
def login():
    return auth_controller.login(request)

@api.route('/auth/register', methods=['POST'])
def register():
    return auth_controller.register(request)

@api.route('/auth/logout', methods=['POST'])
@auth_middleware.require_auth
def logout():
    return auth_controller.logout(request)

# Rutas de usuarios
@api.route('/users/me', methods=['GET'])
@auth_middleware.require_auth
def get_current_user():
    return user_controller.get_current_user(request)

@api.route('/users/me', methods=['PUT'])
@auth_middleware.require_auth
def update_current_user():
    return user_controller.update_current_user(request)

@api.route('/users/<int:user_id>', methods=['GET'])
@auth_middleware.require_auth
def get_user(user_id):
    return user_controller.get_user(user_id)

@api.route('/users/<int:user_id>', methods=['PUT'])
@auth_middleware.require_auth
def update_user(user_id):
    return user_controller.update_user(user_id, request.get_json())

# Rutas de servicios
@api.route('/services', methods=['GET'])
def get_services():
    return service_controller.get_services()

@api.route('/services', methods=['POST'])
@auth_middleware.require_auth
def create_service():
    return service_controller.create_service(request.get_json())

@api.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    return service_controller.get_service(service_id)

@api.route('/services/<int:service_id>', methods=['PUT'])
@auth_middleware.require_auth
def update_service(service_id):
    return service_controller.update_service(service_id, request.get_json())

@api.route('/services/<int:service_id>/image', methods=['POST'])
@auth_middleware.require_auth
def upload_service_image(service_id):
    return service_controller.upload_service_image(service_id)

@api.route('/services/<int:service_id>/image', methods=['GET'])
def get_service_image(service_id):
    return service_controller.get_service_image(service_id)

@api.route('/services/<int:service_id>', methods=['DELETE'])
@auth_middleware.require_auth
def delete_service(service_id):
    return service_controller.delete_service(service_id)

# Rutas de solicitudes
@api.route('/requests', methods=['GET'])
@auth_middleware.require_auth
def get_requests():
    return request_controller.get_requests()

@api.route('/requests', methods=['POST'])
@auth_middleware.require_auth
def create_request():
    return request_controller.create_request(request.get_json())

@api.route('/requests/<int:request_id>', methods=['GET'])
@auth_middleware.require_auth
def get_request(request_id):
    return request_controller.get_request(request_id)

@api.route('/requests/<int:request_id>', methods=['PUT'])
@auth_middleware.require_auth
def update_request(request_id):
    return request_controller.update_request(request_id, request.get_json())

@api.route('/requests/<int:request_id>/cancel', methods=['PUT'])
@auth_middleware.require_auth
def cancel_request(request_id):
    data = request.get_json(force=True, silent=True) or {}
    return request_controller.cancel_request(request_id)
                               
@api.route('/requests/<int:request_id>/accept', methods=['PUT'])
@auth_middleware.require_auth
def accept_request(request_id):
    data = request.get_json(force=True, silent=True) or {}
    data['status'] = 'accepted'
    return request_controller.update_request(request_id, data)

@api.route('/requests/<int:request_id>/reject', methods=['PUT'])
@auth_middleware.require_auth
def reject_request(request_id):
    data = request.get_json(force=True, silent=True) or {}
    data['status'] = 'rejected'
    return request_controller.update_request(request_id, data)

@api.route('/requests/<int:request_id>/complete', methods=['PUT'])
@auth_middleware.require_auth
def complete_request(request_id):
    data = request.get_json(force=True, silent=True) or {}
    data['status'] = 'completed'
    return request_controller.update_request(request_id, data)

@api.route('/requests/<int:request_id>/messages', methods=['GET'])
@auth_middleware.require_auth
def get_request_messages(request_id):
    return message_controller.get_request_messages(request_id)

@api.route('/requests/<int:request_id>/messages', methods=['POST'])
@auth_middleware.require_auth
def create_request_message(request_id):
    return message_controller.create_request_message(request_id, request.get_json())

@api.route('/requests/<int:request_id>/messages/<int:message_id>/read', methods=['PUT'])
@auth_middleware.require_auth
def mark_request_message_as_read(request_id, message_id):
    return message_controller.mark_message_as_read(request_id, message_id)

@api.route('/messages/unread-count', methods=['GET'])
@auth_middleware.require_auth
def get_unread_message_count():
    return message_controller.get_unread_count()

# Rutas de transacciones
@api.route('/transactions', methods=['GET'])
@auth_middleware.require_auth
def get_transactions():
    return transaction_controller.get_transactions()

@api.route('/transactions/<int:transaction_id>', methods=['GET'])
@auth_middleware.require_auth
def get_transaction(transaction_id):
    return transaction_controller.get_transaction(transaction_id)

@api.route('/transactions/transfer', methods=['POST'])
@auth_middleware.require_auth
def transfer_credits():
    return transaction_controller.create_transaction(request.get_json())

@api.route('/transactions/user/<int:user_id>', methods=['GET'])
@auth_middleware.require_auth
def get_user_transactions(user_id):
    return transaction_controller.get_user_transactions(user_id)

@api.route('/payments/stripe/config', methods=['GET'])
@auth_middleware.require_auth
def get_stripe_config():
    return transaction_controller.get_stripe_public_config()

@api.route('/payments/stripe/payment-intent', methods=['POST'])
@auth_middleware.require_auth
def create_stripe_payment_intent():
    return transaction_controller.create_stripe_payment_intent(request.get_json())

@api.route('/payments/stripe/confirm', methods=['POST'])
@auth_middleware.require_auth
def confirm_stripe_payment():
    return transaction_controller.confirm_stripe_payment(request.get_json())

@api.route('/payments/stripe/webhook', methods=['POST'])
def stripe_webhook():
    raw_payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature', '')
    return transaction_controller.handle_stripe_webhook(raw_payload, sig_header)

# Rutas de administración
@api.route('/admin/stats', methods=['GET'])
@auth_middleware.require_auth
@auth_middleware.require_admin
def get_stats():
    return admin_controller.get_stats()

@api.route('/admin/users', methods=['GET'])
@auth_middleware.require_auth
@auth_middleware.require_admin
def get_all_users():
    return admin_controller.get_all_users(request)

@api.route('/admin/users/<int:user_id>/credits', methods=['POST'])
@auth_middleware.require_auth
@auth_middleware.require_admin
def manage_user_credits(user_id):
    data = request.get_json() or {}
    return admin_controller.manage_credits(user_id, data.get('amount', 0))

@api.route('/admin/users/<int:user_id>/toggle-status', methods=['PUT'])
@auth_middleware.require_auth
@auth_middleware.require_admin
def toggle_user_status(user_id):
    current_user_id = request.user.get('user_id')
    return admin_controller.toggle_user_status(user_id, current_user_id)

@api.route('/admin/services/<int:service_id>/approve', methods=['PUT'])
@auth_middleware.require_auth
@auth_middleware.require_admin
def approve_service(service_id):
    return admin_controller.approve_service(service_id)

@api.route('/admin/services/<int:service_id>/reject', methods=['PUT'])
@auth_middleware.require_auth
@auth_middleware.require_admin
def reject_service(service_id):
    return admin_controller.reject_service(service_id)

# Rutas de valoraciones
@api.route('/services/<int:service_id>/reviews', methods=['GET'])
def get_service_reviews(service_id):
    return review_controller.get_service_reviews(service_id)

@api.route('/reviews', methods=['POST'])
@auth_middleware.require_auth
def create_review():
    return review_controller.create_review(request.get_json())

@api.route('/reviews/<int:review_id>', methods=['DELETE'])
@auth_middleware.require_auth
@auth_middleware.require_admin
def delete_review(review_id):
    return review_controller.delete_review(review_id)

def register_routes(app):
    """Registra todas las rutas en la aplicación"""
    app.register_blueprint(api, url_prefix='/api')
