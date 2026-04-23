/**
 * API Service
 * Maneja todas las peticiones HTTP al backend
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// ============ AUTENTICACIÓN ============

export const login = async (credentials) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al iniciar sesión');
  }
  return response.json();
};

export const register = async (userData) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error en el registro');
  }
  return response.json();
};

export const logout = async () => {
  try {
    const token = localStorage.getItem('token');
    if (token) {
      await fetch(`${API_URL}/auth/logout`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` 
        }
      });
    }
  } catch (error) {
    console.error('Error during logout request:', error);
  } finally {
    localStorage.removeItem('token');
  }
};

// ============ USUARIOS ============

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
};

export const getUser = async (userId) => {
  const response = await fetch(`${API_URL}/users/${userId}`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    throw new Error('Error al obtener el usuario');
  }
  return response.json();
};

export const getCurrentUser = async () => {
  const response = await fetch(`${API_URL}/users/me`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    throw new Error('Error al obtener tu perfil');
  }
  return response.json();
};

export const updateUser = async (userId, userData) => {
  const response = await fetch(`${API_URL}/users/${userId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(userData)
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al actualizar el usuario');
  }
  return response.json();
};

export const getUserBalance = async () => {
  const response = await fetch(`${API_URL}/users/me`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    throw new Error('Error al obtener el balance');
  }
  const data = await response.json();
  return data.balance ?? 0;
};

// ============ SERVICIOS ============

export const getServices = async (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.category) params.append('category', filters.category);
  if (filters.search) params.append('search', filters.search);
  if (filters.status) params.append('status', filters.status);
  if (filters.page) params.append('page', filters.page);
  if (filters.per_page) params.append('per_page', filters.per_page);

  const url = `${API_URL}/services${params.toString() ? '?' + params.toString() : ''}`;
  const response = await fetch(url, { method: 'GET', headers: getAuthHeaders() });
  if (!response.ok) {
    throw new Error('Error al obtener servicios');
  }
  return response.json();
};

export const getService = async (serviceId) => {
  const response = await fetch(`${API_URL}/services/${serviceId}`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Servicio no encontrado');
  }
  return response.json();
};

export const createService = async (serviceData) => {
  const response = await fetch(`${API_URL}/services`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(serviceData)
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al crear el servicio');
  }
  return response.json();
};

export const updateService = async (serviceId, serviceData) => {
  const response = await fetch(`${API_URL}/services/${serviceId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(serviceData)
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al actualizar el servicio');
  }
  return response.json();
};

export const deleteService = async (serviceId) => {
  const response = await fetch(`${API_URL}/services/${serviceId}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al eliminar el servicio');
  }
  return response.json();
};

// ============ SOLICITUDES ============

export const getRequests = async (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.status) params.append('status', filters.status);
  if (filters.service_id) params.append('service_id', filters.service_id);
  if (filters.page) params.append('page', filters.page);
  if (filters.per_page) params.append('per_page', filters.per_page);

  const url = `${API_URL}/requests${params.toString() ? '?' + params.toString() : ''}`;
  const response = await fetch(url, { method: 'GET', headers: getAuthHeaders() });
  if (!response.ok) {
    throw new Error('Error al obtener solicitudes');
  }
  return response.json();
};

export const createRequest = async (requestData) => {
  const response = await fetch(`${API_URL}/requests`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(requestData)
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al crear la solicitud');
  }
  return response.json();
};

export const acceptRequest = async (requestId) => {
  const response = await fetch(`${API_URL}/requests/${requestId}/accept`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify({})
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al aceptar la solicitud');
  }
  return response.json();
};

export const rejectRequest = async (requestId) => {
  const response = await fetch(`${API_URL}/requests/${requestId}/reject`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify({})
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al rechazar la solicitud');
  }
  return response.json();
};

export const cancelRequest = async (requestId) => {
  const response = await fetch(`${API_URL}/requests/${requestId}/cancel`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify({})
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al cancelar la solicitud');
  }
  return response.json();
};

export const completeRequest = async (requestId) => {
  const response = await fetch(`${API_URL}/requests/${requestId}/complete`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify({})
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al completar la solicitud');
  }
  return response.json();
};

export const updateRequestStatus = async (requestId, status) => {
  const actions = { accepted: acceptRequest, rejected: rejectRequest, cancelled: cancelRequest, completed: completeRequest };
  if (actions[status]) return actions[status](requestId);
  const response = await fetch(`${API_URL}/requests/${requestId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify({ status })
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al actualizar la solicitud');
  }
  return response.json();
};

// ============ TRANSACCIONES ============

export const getTransactions = async (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.type) params.append('type', filters.type);
  if (filters.page) params.append('page', filters.page);
  if (filters.per_page) params.append('per_page', filters.per_page);

  const url = `${API_URL}/transactions${params.toString() ? '?' + params.toString() : ''}`;
  const response = await fetch(url, { method: 'GET', headers: getAuthHeaders() });
  if (!response.ok) {
    throw new Error('Error al obtener transacciones');
  }
  return response.json();
};

export const transferCredits = async (transferData) => {
  const response = await fetch(`${API_URL}/transactions/transfer`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(transferData)
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al realizar la transferencia');
  }
  return response.json();
};

export const getUserTransactions = async (userId, filters = {}) => {
  const params = new URLSearchParams();
  if (filters.page) params.append('page', filters.page);
  if (filters.per_page) params.append('per_page', filters.per_page);

  const url = `${API_URL}/transactions/user/${userId}${params.toString() ? '?' + params.toString() : ''}`;
  const response = await fetch(url, { method: 'GET', headers: getAuthHeaders() });
  if (!response.ok) {
    throw new Error('Error al obtener transacciones del usuario');
  }
  return response.json();
};

// ============ REVIEWS ============

export const getServiceReviews = async (serviceId) => {
  const response = await fetch(`${API_URL}/services/${serviceId}/reviews`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    return [];
  }
  return response.json();
};

export const createReview = async (reviewData) => {
  const response = await fetch(`${API_URL}/reviews`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(reviewData)
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || 'Error al crear la reseña');
  }
  return response.json();
};

// ============ ADMINISTRACIÓN ============

export const getAdminStats = async () => {
  const response = await fetch(`${API_URL}/admin/stats`, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    throw new Error('Error al obtener estadísticas');
  }
  return response.json();
};

export const getAllUsers = async (search = '') => {
  const url = `${API_URL}/admin/users${search ? `?search=${encodeURIComponent(search)}` : ''}`;
  const response = await fetch(url, {
    method: 'GET',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    throw new Error('Error al obtener usuarios');
  }
  return response.json();
};

export const adminAdjustCredits = async (userId, amount) => {
  const response = await fetch(`${API_URL}/admin/users/${userId}/credits`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ amount })
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.error || 'Error al ajustar créditos');
  }
  return response.json();
};

export const adminApproveService = async (serviceId) => {
  const response = await fetch(`${API_URL}/admin/services/${serviceId}/approve`, {
    method: 'PUT',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.error || 'Error al activar servicio');
  }
  return response.json();
};

export const adminRejectService = async (serviceId) => {
  const response = await fetch(`${API_URL}/admin/services/${serviceId}/reject`, {
    method: 'PUT',
    headers: getAuthHeaders()
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.error || 'Error al desactivar servicio');
  }
  return response.json();
};