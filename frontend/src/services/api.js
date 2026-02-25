/**
 * API Service
 * Maneja todas las peticiones HTTP al backend
 * TODO: Implementar todas las funciones de API
 */

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// ============ AUTENTICACIÓN ============

export const login = async (credentials) => {
  // TODO: Implementar login
  throw new Error('Login no implementado');
};

export const register = async (userData) => {
  // TODO: Implementar registro
  throw new Error('Registro no implementado');
};

export const logout = () => {
  // TODO: Implementar logout
  localStorage.removeItem('token');
};

// ============ USUARIOS ============

export const getUser = async (userId) => {
  // TODO: Implementar obtener usuario
  throw new Error('Obtener usuario no implementado');
};

export const updateUser = async (userId, userData) => {
  // TODO: Implementar actualizar usuario
  throw new Error('Actualizar usuario no implementado');
};

export const getUserBalance = async (userId) => {
  // TODO: Implementar obtener balance
  throw new Error('Obtener balance no implementado');
};

// ============ SERVICIOS ============

export const getServices = async (filters = {}) => {
  // TODO: Implementar obtener servicios
  return [];
};

export const getService = async (serviceId) => {
  // TODO: Implementar obtener servicio específico
  throw new Error('Obtener servicio no implementado');
};

export const createService = async (serviceData) => {
  // TODO: Implementar crear servicio
  throw new Error('Crear servicio no implementado');
};

export const updateService = async (serviceId, serviceData) => {
  // TODO: Implementar actualizar servicio
  throw new Error('Actualizar servicio no implementado');
};

export const deleteService = async (serviceId) => {
  // TODO: Implementar eliminar servicio
  throw new Error('Eliminar servicio no implementado');
};

// ============ SOLICITUDES ============

export const getRequests = async (filters = {}) => {
  // TODO: Implementar obtener solicitudes
  return [];
};

export const createRequest = async (requestData) => {
  // TODO: Implementar crear solicitud
  throw new Error('Crear solicitud no implementado');
};

export const updateRequestStatus = async (requestId, status) => {
  // TODO: Implementar actualizar estado de solicitud
  throw new Error('Actualizar solicitud no implementado');
};

// ============ REVIEWS ============

export const getServiceReviews = async (serviceId) => {
  // TODO: Implementar obtener reviews de servicio
  return [];
};

export const createReview = async (reviewData) => {
  // TODO: Implementar crear review
  throw new Error('Crear review no implementado');
};

// ============ ADMINISTRACIÓN ============

export const getAdminStats = async () => {
  // TODO: Implementar obtener estadísticas de admin
  throw new Error('Estadísticas de admin no implementadas');
};

export const getAllUsers = async () => {
  // TODO: Implementar obtener todos los usuarios
  return [];
};

export const approveService = async (serviceId) => {
  // TODO: Implementar aprobar servicio
  throw new Error('Aprobar servicio no implementado');
};

export const rejectService = async (serviceId) => {
  // TODO: Implementar rechazar servicio
  throw new Error('Rechazar servicio no implementado');
};