import React, { useState, useEffect, useCallback } from 'react';
import {
  getAdminStats,
  getAllUsers,
  adminAdjustCredits,
  getServices,
  adminApproveService,
  adminRejectService,
} from '../services/api';
import './AdminPanel.css';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('stats');

  // Stats
  const [stats, setStats] = useState(null);
  const [loadingStats, setLoadingStats] = useState(true);

  // Users
  const [users, setUsers] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [userSearch, setUserSearch] = useState('');

  // Services
  const [services, setServices] = useState([]);
  const [loadingServices, setLoadingServices] = useState(false);

  // Credit modal
  const [creditModal, setCreditModal] = useState(null);
  const [creditAmount, setCreditAmount] = useState('');
  const [creditError, setCreditError] = useState(null);
  const [adjusting, setAdjusting] = useState(false);

  const [error, setError] = useState(null);

  // ── Fetch ───────────────────────────────────────────────────────────────

  const fetchStats = useCallback(async () => {
    try {
      setLoadingStats(true);
      setError(null);
      const data = await getAdminStats();
      setStats(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoadingStats(false);
    }
  }, []);

  const fetchUsers = useCallback(async (search = '') => {
    try {
      setLoadingUsers(true);
      setError(null);
      const data = await getAllUsers(search);
      setUsers(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoadingUsers(false);
    }
  }, []);

  const fetchServices = useCallback(async () => {
    try {
      setLoadingServices(true);
      setError(null);
      const data = await getServices({ per_page: 100 });
      // getServices devuelve { items: [], total, page, per_page }
      setServices(Array.isArray(data) ? data : (data.items ?? data.services ?? []));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoadingServices(false);
    }
  }, []);

  useEffect(() => { fetchStats(); }, [fetchStats]);

  useEffect(() => {
    if (activeTab === 'users') fetchUsers();
    if (activeTab === 'services') fetchServices();
  }, [activeTab, fetchUsers, fetchServices]);

  // ── Handlers ────────────────────────────────────────────────────────────

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchUsers(userSearch);
  };

  const openCreditModal = (u) => {
    setCreditModal(u);
    setCreditAmount('');
    setCreditError(null);
  };

  const handleAdjustCredits = async (e) => {
    e.preventDefault();
    const amount = Number.parseInt(creditAmount, 10);
    if (Number.isNaN(amount) || amount === 0) {
      setCreditError('Introduce un número distinto de 0');
      return;
    }
    try {
      setAdjusting(true);
      setCreditError(null);
      await adminAdjustCredits(creditModal.id, amount);
      setCreditModal(null);
      fetchUsers(userSearch);
    } catch (err) {
      setCreditError(err.message);
    } finally {
      setAdjusting(false);
    }
  };

  const handleApprove = async (serviceId) => {
    try {
      setError(null);
      await adminApproveService(serviceId);
      fetchServices();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleReject = async (serviceId) => {
    try {
      setError(null);
      await adminRejectService(serviceId);
      fetchServices();
    } catch (e) {
      setError(e.message);
    }
  };

  const formatDate = (iso) => {
    if (!iso) return '—';
    return new Date(iso).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' });
  };

  const sumByStatus = (obj) =>
    Object.values(obj ?? {}).reduce((a, b) => a + b, 0);

  // ── Render ──────────────────────────────────────────────────────────────

  return (
    <div className="module-container">
      <h1>Panel de Administración</h1>
      <p className="subtitle">Gestión global del sistema Time Bank</p>

      {error && <div className="alert alert-error">{error}</div>}

      {/* Tabs */}
      <div className="admin-tabs">
        <button
          className={`tab-btn${activeTab === 'stats' ? ' active' : ''}`}
          onClick={() => setActiveTab('stats')}
        >📊 Estadísticas</button>
        <button
          className={`tab-btn${activeTab === 'users' ? ' active' : ''}`}
          onClick={() => setActiveTab('users')}
        >👥 Usuarios</button>
        <button
          className={`tab-btn${activeTab === 'services' ? ' active' : ''}`}
          onClick={() => setActiveTab('services')}
        >🛠 Servicios</button>
      </div>

      {/* ── Stats ── */}
      {activeTab === 'stats' && (
        loadingStats
          ? <div className="loading-state">Cargando estadísticas...</div>
          : stats && (
            <>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-icon">👥</div>
                  <div className="stat-value">{stats.users?.total ?? 0}</div>
                  <div className="stat-label">Usuarios totales</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">🛡️</div>
                  <div className="stat-value">{stats.users?.admins ?? 0}</div>
                  <div className="stat-label">Administradores</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">🛠</div>
                  <div className="stat-value">{sumByStatus(stats.services?.by_status)}</div>
                  <div className="stat-label">Servicios totales</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">✅</div>
                  <div className="stat-value">{stats.services?.by_status?.active ?? 0}</div>
                  <div className="stat-label">Servicios activos</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">📋</div>
                  <div className="stat-value">{sumByStatus(stats.requests?.by_status)}</div>
                  <div className="stat-label">Solicitudes totales</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">⏱️</div>
                  <div className="stat-value">{stats.transactions?.total ?? 0}</div>
                  <div className="stat-label">Transacciones</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">💰</div>
                  <div className="stat-value">{stats.transactions?.credits_sum ?? 0}</div>
                  <div className="stat-label">Créditos movidos</div>
                </div>
              </div>

              <h2 className="section-title" style={{ marginTop: '1.5rem' }}>Solicitudes por estado</h2>
              <div className="stats-grid">
                {Object.entries(stats.requests?.by_status ?? {}).map(([status, count]) => (
                  <div className="stat-card" key={status}>
                    <div className="stat-value">{count}</div>
                    <div className="stat-label">{status}</div>
                  </div>
                ))}
              </div>
            </>
          )
      )}

      {/* ── Users ── */}
      {activeTab === 'users' && (
        <>
          <form className="admin-search-form" onSubmit={handleSearchSubmit}>
            <input
              type="text"
              className="admin-search-input"
              placeholder="Buscar por nombre o email..."
              value={userSearch}
              onChange={(e) => setUserSearch(e.target.value)}
            />
            <button type="submit" className="btn-primary btn-sm">Buscar</button>
            {userSearch && (
              <button
                type="button"
                className="btn-outline btn-sm"
                onClick={() => { setUserSearch(''); fetchUsers(''); }}
              >Limpiar</button>
            )}
          </form>

          {loadingUsers
            ? <div className="loading-state">Cargando usuarios...</div>
            : (
              <div className="admin-table-wrapper">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Nombre</th>
                      <th>Email</th>
                      <th>Rol</th>
                      <th>Saldo</th>
                      <th>Registro</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.length === 0
                      ? <tr><td colSpan={7} className="empty-cell">No se encontraron usuarios</td></tr>
                      : users.map(u => (
                        <tr key={u.id}>
                          <td className="tx-id">{u.id}</td>
                          <td><strong>{u.name}</strong></td>
                          <td style={{ color: 'var(--text-secondary)' }}>{u.email}</td>
                          <td><span className={`role-badge role-${u.role}`}>{u.role}</span></td>
                          <td><span className="balance-chip">⏱ {u.balance}</span></td>
                          <td className="tx-date">{formatDate(u.created_at)}</td>
                          <td>
                            <button
                              className="btn-primary btn-sm"
                              onClick={() => openCreditModal(u)}
                            >
                              Ajustar créditos
                            </button>
                          </td>
                        </tr>
                      ))
                    }
                  </tbody>
                </table>
              </div>
            )
          }
        </>
      )}

      {/* ── Services ── */}
      {activeTab === 'services' && (
        loadingServices
          ? <div className="loading-state">Cargando servicios...</div>
          : (
            <div className="admin-table-wrapper">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Título</th>
                    <th>Categoría</th>
                    <th>Créditos</th>
                    <th>Estado</th>
                    <th>Propietario</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {services.length === 0
                    ? <tr><td colSpan={7} className="empty-cell">No hay servicios</td></tr>
                    : services.map(s => (
                      <tr key={s.id}>
                        <td className="tx-id">{s.id}</td>
                        <td><strong>{s.title}</strong></td>
                        <td style={{ color: 'var(--text-secondary)' }}>{s.category || '—'}</td>
                        <td>⏱ {s.credits ?? 1}</td>
                        <td><span className={`status-badge status-${s.status}`}>{s.status}</span></td>
                        <td style={{ color: 'var(--text-secondary)' }}>{s.owner_name || `#${s.owner_id}`}</td>
                        <td>
                          <div className="action-buttons">
                            {s.status !== 'active' && s.status !== 'deleted' && (
                              <button
                                className="btn-success btn-sm"
                                onClick={() => handleApprove(s.id)}
                              >
                                Activar
                              </button>
                            )}
                            {s.status === 'active' && (
                              <button
                                className="btn-danger btn-sm"
                                onClick={() => handleReject(s.id)}
                              >
                                Desactivar
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))
                  }
                </tbody>
              </table>
            </div>
          )
      )}

      {/* ── Modal ajuste de créditos ── */}
      {creditModal && (
        <div className="modal-overlay">
          <dialog
            className="modal"
            open
            onClose={() => setCreditModal(null)}
          >
            <div className="modal-header">
              <h2>Ajustar créditos</h2>
              <button className="modal-close" onClick={() => setCreditModal(null)}>×</button>
            </div>
            <form className="modal-form" onSubmit={handleAdjustCredits}>
              <p className="credit-modal-info">
                Usuario: <strong>{creditModal.name}</strong> — Saldo actual:{' '}
                <strong>⏱ {creditModal.balance}</strong>
              </p>
              {creditError && <div className="alert alert-error">{creditError}</div>}
              <div className="form-group">
                <label htmlFor="creditAmount">
                  Cantidad <span className="label-hint">(positivo para añadir, negativo para quitar)</span>
                </label>
                <input
                  id="creditAmount"
                  type="number"
                  value={creditAmount}
                  onChange={(e) => setCreditAmount(e.target.value)}
                  placeholder="Ej: 10 o -5"
                  autoFocus
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-outline" onClick={() => setCreditModal(null)}>
                  Cancelar
                </button>
                <button type="submit" className="btn-primary" disabled={adjusting}>
                  {adjusting ? 'Aplicando...' : 'Aplicar ajuste'}
                </button>
              </div>
            </form>
          </dialog>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;

