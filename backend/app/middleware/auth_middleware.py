"""
Auth Middleware
Middleware para validación de autenticación
"""

from functools import wraps
from flask import request, jsonify

class AuthMiddleware:
    def __init__(self, auth_service):
        self.auth_service = auth_service
    
    def require_auth(self, f):
        """Decorator para requerir autenticación"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token:
                return jsonify({'error': 'No token provided'}), 401
            
            # Remover 'Bearer ' si está presente
            if token.startswith('Bearer '):
                token = token[7:]
            
            payload = self.auth_service.verify_token(token)
            
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            request.user = payload
            return f(*args, **kwargs)
        
        return decorated_function
    
    def require_admin(self, f):
        """Decorator para requerir permisos de administrador"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'user'):
                return jsonify({'error': 'Unauthorized'}), 401
            
            if request.user.get('role') != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
