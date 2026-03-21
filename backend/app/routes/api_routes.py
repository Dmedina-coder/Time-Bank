"""
API Routes
Define todas las rutas de la API
"""

from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import AuthController
from app.controllers.user_controller import UserController
from app.controllers.admin_controller import AdminController
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
    pass

@api.route('/services', methods=['POST'])
def create_service():
    pass

@api.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    pass

@api.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    pass

@api.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    pass

# Rutas de solicitudes
@api.route('/requests', methods=['GET'])
def get_requests():
    pass

@api.route('/requests', methods=['POST'])
def create_request():
    pass

@api.route('/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    pass

# Rutas de transacciones
@api.route('/transactions', methods=['GET'])
def get_transactions():
    pass

@api.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    pass

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

def register_routes(app):
    """Registra todas las rutas en la aplicación"""
    app.register_blueprint(api, url_prefix='/api')
