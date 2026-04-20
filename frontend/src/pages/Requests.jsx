import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import * as api from '../services/api';
import './Requests.css';

const STATUS_LABELS = {
  pending: 'Pendiente',
  accepted: 'Aceptada',
  rejected: 'Rechazada',
  cancelled: 'Cancelada',
  completed: 'Completada'
};

const STATUS_CLASSES = {
  pending: 'status-pending',
  accepted: 'status-accepted',
  rejected: 'status-rejected',
  cancelled: 'status-cancelled',
  completed: 'status-completed'
};

const Requests = () => {
  const { user } = useContext(AuthContext);

  const [requests, setRequests] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const perPage = 10;

  const [statusFilter, setStatusFilter] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [actionError, setActionError] = useState(null);
  const [actionLoading, setActionLoading] = useState(null); // requestId being processed

  const fetchRequests = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getRequests({
        status: statusFilter || undefined,
        page,
        per_page: perPage
      });
      setRequests(data.items || []);
      setTotal(data.total || 0);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRequests();
  }, [statusFilter, page]);

  const handleAction = async (requestId, action) => {
    try {
      setActionLoading(requestId);
      setActionError(null);
      switch (action) {
        case 'accept':   await api.acceptRequest(requestId);   break;
        case 'reject':   await api.rejectRequest(requestId);   break;
        case 'cancel':   await api.cancelRequest(requestId);   break;
        case 'complete': await api.completeRequest(requestId); break;
        default: break;
      }
      fetchRequests();
    } catch (err) {
      setActionError(err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const totalPages = Math.ceil(total / perPage);

  const getActions = (req) => {
    const isRequester = req.requester_id === user?.id;
    const isProvider  = req.provider_id  === user?.id;
    const actions = [];

    if (req.status === 'pending') {
      if (isProvider) {
        actions.push({ label: 'Aceptar', action: 'accept', cls: 'btn-success' });
        actions.push({ label: 'Rechazar', action: 'reject', cls: 'btn-danger' });
      }
      if (isRequester) {
        actions.push({ label: 'Cancelar', action: 'cancel', cls: 'btn-outline-danger' });
      }
    }
    if (req.status === 'accepted' && isProvider) {
      actions.push({ label: 'Marcar completada', action: 'complete', cls: 'btn-success' });
    }
    if (req.status === 'accepted' && isRequester) {
      actions.push({ label: 'Cancelar', action: 'cancel', cls: 'btn-outline-danger' });
    }
    return actions;
  };

  return (
    <div className="requests-page">
      <div className="requests-header">
        <div>
          <h1>Solicitudes</h1>
          <p className="subtitle">Gestiona las solicitudes de servicios</p>
        </div>
      </div>

      {/* Filtro por estado */}
      <div className="requests-filters">
        <select
          value={statusFilter}
          onChange={e => { setStatusFilter(e.target.value); setPage(1); }}
          className="filter-select"
        >
          <option value="">Todos los estados</option>
          {Object.entries(STATUS_LABELS).map(([val, label]) => (
            <option key={val} value={val}>{label}</option>
          ))}
        </select>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {actionError && <div className="alert alert-error">{actionError}</div>}

      {loading ? (
        <div className="loading-state">Cargando solicitudes...</div>
      ) : requests.length === 0 ? (
        <div className="empty-state-block">
          <p>No hay solicitudes que mostrar.</p>
          <Link to="/services" className="btn-primary">Ver servicios disponibles</Link>
        </div>
      ) : (
        <>
          <div className="requests-table-wrapper">
            <table className="requests-table">
              <thead>
                <tr>
                  <th>Servicio</th>
                  <th>Solicitante</th>
                  <th>Proveedor</th>
                  <th>Fecha programada</th>
                  <th>Estado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {requests.map(req => {
                  const actions = getActions(req);
                  return (
                    <tr key={req.id}>
                      <td>
                        <Link to={`/services/${req.service_id}`} className="table-link">
                          {req.service_title || `Servicio #${req.service_id}`}
                        </Link>
                      </td>
                      <td>
                        <span className={req.requester_id === user?.id ? 'me-badge' : ''}>
                          {req.requester_name}
                          {req.requester_id === user?.id && ' (yo)'}
                        </span>
                      </td>
                      <td>
                        <span className={req.provider_id === user?.id ? 'me-badge' : ''}>
                          {req.provider_name}
                          {req.provider_id === user?.id && ' (yo)'}
                        </span>
                      </td>
                      <td>
                        {req.scheduled_date
                          ? new Date(req.scheduled_date).toLocaleString('es-ES', { dateStyle: 'medium', timeStyle: 'short' })
                          : '—'}
                      </td>
                      <td>
                        <span className={`status-badge ${STATUS_CLASSES[req.status] || ''}`}>
                          {STATUS_LABELS[req.status] || req.status}
                        </span>
                      </td>
                      <td>
                        <div className="action-buttons">
                          {actions.map(({ label, action, cls }) => (
                            <button
                              key={action}
                              className={`btn-action ${cls}`}
                              disabled={actionLoading === req.id}
                              onClick={() => handleAction(req.id, action)}
                            >
                              {actionLoading === req.id ? '...' : label}
                            </button>
                          ))}
                          {actions.length === 0 && <span className="no-actions">—</span>}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {totalPages > 1 && (
            <div className="pagination">
              <button disabled={page === 1} onClick={() => setPage(p => p - 1)} className="btn-outline btn-sm">
                ← Anterior
              </button>
              <span className="page-info">Página {page} de {totalPages} ({total} solicitudes)</span>
              <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)} className="btn-outline btn-sm">
                Siguiente →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Requests;
