import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import * as api from '../services/api';
import './Services.css';

const CATEGORIES = ['tecnología', 'educación', 'hogar', 'salud', 'transporte', 'arte', 'otros'];

const initialForm = { title: '', description: '', category: '' };

const Services = () => {
  const { user } = useContext(AuthContext);

  const [services, setServices] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const perPage = 12;

  const [filters, setFilters] = useState({ search: '', category: '', status: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Modal crear/editar
  const [showModal, setShowModal] = useState(false);
  const [editingService, setEditingService] = useState(null);
  const [form, setForm] = useState(initialForm);
  const [formError, setFormError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const fetchServices = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getServices({ ...filters, page, per_page: perPage });
      setServices(data.items || []);
      setTotal(data.total || 0);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchServices();
  }, [filters, page]);

  const handleFilterChange = (e) => {
    setFilters(prev => ({ ...prev, [e.target.name]: e.target.value }));
    setPage(1);
  };

  const openCreate = () => {
    setEditingService(null);
    setForm(initialForm);
    setFormError(null);
    setShowModal(true);
  };

  const openEdit = (service) => {
    setEditingService(service);
    setForm({ title: service.title, description: service.description, category: service.category });
    setFormError(null);
    setShowModal(true);
  };

  const handleFormChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title.trim() || !form.description.trim() || !form.category.trim()) {
      setFormError('Todos los campos son obligatorios.');
      return;
    }
    try {
      setSubmitting(true);
      setFormError(null);
      if (editingService) {
        await api.updateService(editingService.id, form);
      } else {
        await api.createService(form);
      }
      setShowModal(false);
      fetchServices();
    } catch (err) {
      setFormError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (service) => {
    if (!window.confirm(`¿Eliminar el servicio "${service.title}"?`)) return;
    try {
      await api.deleteService(service.id);
      fetchServices();
    } catch (err) {
      alert(err.message);
    }
  };

  const totalPages = Math.ceil(total / perPage);

  const statusLabel = { active: 'Activo', inactive: 'Inactivo' };
  const statusClass = { active: 'status-accepted', inactive: 'status-cancelled' };

  return (
    <div className="services-page">
      <div className="services-header">
        <div>
          <h1>Servicios</h1>
          <p className="subtitle">Descubre y ofrece servicios en tu comunidad</p>
        </div>
        <button className="btn-primary" onClick={openCreate}>+ Publicar servicio</button>
      </div>

      {/* Filtros */}
      <div className="services-filters">
        <input
          type="text"
          name="search"
          placeholder="Buscar servicios..."
          value={filters.search}
          onChange={handleFilterChange}
          className="filter-input"
        />
        <select name="category" value={filters.category} onChange={handleFilterChange} className="filter-select">
          <option value="">Todas las categorías</option>
          {CATEGORIES.map(c => <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>)}
        </select>
        <select name="status" value={filters.status} onChange={handleFilterChange} className="filter-select">
          <option value="">Todos los estados</option>
          <option value="active">Activos</option>
          <option value="inactive">Inactivos</option>
        </select>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {loading ? (
        <div className="loading-state">Cargando servicios...</div>
      ) : services.length === 0 ? (
        <div className="empty-services">
          <p>No se encontraron servicios.</p>
          <button className="btn-primary" onClick={openCreate}>Sé el primero en publicar</button>
        </div>
      ) : (
        <>
          <div className="services-grid">
            {services.map(service => (
              <div key={service.id} className="service-card-item">
                <div className="service-card-body">
                  <div className="service-card-top">
                    <span className="service-category">{service.category}</span>
                    <span className={`status-badge ${statusClass[service.status] || ''}`}>
                      {statusLabel[service.status] || service.status}
                    </span>
                  </div>
                  <h3 className="service-title">
                    <Link to={`/services/${service.id}`}>{service.title}</Link>
                  </h3>
                  <p className="service-description">{service.description}</p>
                  <p className="service-owner">Por: {service.owner_name}</p>
                </div>
                <div className="service-card-actions">
                  <Link to={`/services/${service.id}`} className="btn-outline btn-sm">Ver detalles</Link>
                  {user?.id === service.owner_id && (
                    <>
                      <button className="btn-secondary btn-sm" onClick={() => openEdit(service)}>Editar</button>
                      <button className="btn-danger btn-sm" onClick={() => handleDelete(service)}>Eliminar</button>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* Paginación */}
          {totalPages > 1 && (
            <div className="pagination">
              <button disabled={page === 1} onClick={() => setPage(p => p - 1)} className="btn-outline btn-sm">
                ← Anterior
              </button>
              <span className="page-info">Página {page} de {totalPages} ({total} servicios)</span>
              <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)} className="btn-outline btn-sm">
                Siguiente →
              </button>
            </div>
          )}
        </>
      )}

      {/* Modal crear/editar */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingService ? 'Editar servicio' : 'Publicar nuevo servicio'}</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>✕</button>
            </div>
            <form onSubmit={handleSubmit} className="modal-form">
              {formError && <div className="alert alert-error">{formError}</div>}
              <div className="form-group">
                <label>Título</label>
                <input
                  type="text"
                  name="title"
                  value={form.title}
                  onChange={handleFormChange}
                  placeholder="Ej: Clases de guitarra"
                  required
                />
              </div>
              <div className="form-group">
                <label>Descripción</label>
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleFormChange}
                  placeholder="Describe tu servicio con detalle..."
                  rows={4}
                  required
                />
              </div>
              <div className="form-group">
                <label>Categoría</label>
                <select name="category" value={form.category} onChange={handleFormChange} required>
                  <option value="">Selecciona una categoría</option>
                  {CATEGORIES.map(c => <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>)}
                </select>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-outline" onClick={() => setShowModal(false)}>Cancelar</button>
                <button type="submit" className="btn-primary" disabled={submitting}>
                  {submitting ? 'Guardando...' : (editingService ? 'Guardar cambios' : 'Publicar')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Services;
