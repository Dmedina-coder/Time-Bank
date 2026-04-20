import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import * as api from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const [balance, setBalance] = useState(null);
  const [recentServices, setRecentServices] = useState([]);
  const [recentRequests, setRecentRequests] = useState([]);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [profileData, servicesData, requestsData, transactionsData] = await Promise.allSettled([
          api.getCurrentUser(),
          api.getServices({ per_page: 5 }),
          api.getRequests({ per_page: 5 }),
          api.getTransactions({ per_page: 5 })
        ]);

        if (profileData.status === 'fulfilled') {
          setBalance(profileData.value.balance ?? 0);
        }
        if (servicesData.status === 'fulfilled') {
          setRecentServices(servicesData.value.items || []);
        }
        if (requestsData.status === 'fulfilled') {
          setRecentRequests(requestsData.value.items || []);
        }
        if (transactionsData.status === 'fulfilled') {
          setRecentTransactions(transactionsData.value.items || []);
        }
      } catch (err) {
        setError('Error al cargar el dashboard');
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  const statusLabel = {
    pending: 'Pendiente',
    accepted: 'Aceptada',
    rejected: 'Rechazada',
    cancelled: 'Cancelada',
    completed: 'Completada'
  };

  const statusClass = {
    pending: 'status-pending',
    accepted: 'status-accepted',
    rejected: 'status-rejected',
    cancelled: 'status-cancelled',
    completed: 'status-completed'
  };

  if (loading) return <div className="loading-state">Cargando dashboard...</div>;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Bienvenido, {user?.username || user?.name}</h1>
        <p className="dashboard-subtitle">Tu panel personal del Banco de Tiempo</p>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {/* Balance Card */}
      <div className="dashboard-balance-card">
        <div className="balance-icon">⏱</div>
        <div className="balance-info">
          <span className="balance-label">Tu saldo de créditos</span>
          <span className="balance-amount">{balance ?? '—'} créditos</span>
        </div>
        <Link to="/transactions" className="btn-secondary btn-sm">Ver historial</Link>
      </div>

      <div className="dashboard-grid">
        {/* Últimos servicios */}
        <div className="dashboard-card">
          <div className="card-header">
            <h2>Últimos Servicios</h2>
            <Link to="/services" className="link-more">Ver todos →</Link>
          </div>
          {recentServices.length === 0 ? (
            <p className="empty-state">No hay servicios disponibles.</p>
          ) : (
            <ul className="dashboard-list">
              {recentServices.map(s => (
                <li key={s.id}>
                  <Link to={`/services/${s.id}`} className="list-item-title">{s.title}</Link>
                  <span className="list-item-meta">{s.category} · {s.owner_name}</span>
                </li>
              ))}
            </ul>
          )}
          <Link to="/services" className="btn-primary btn-sm mt-1">Publicar servicio</Link>
        </div>

        {/* Mis solicitudes */}
        <div className="dashboard-card">
          <div className="card-header">
            <h2>Mis Solicitudes</h2>
            <Link to="/requests" className="link-more">Ver todas →</Link>
          </div>
          {recentRequests.length === 0 ? (
            <p className="empty-state">No tienes solicitudes recientes.</p>
          ) : (
            <ul className="dashboard-list">
              {recentRequests.map(r => (
                <li key={r.id}>
                  <span className="list-item-title">{r.service_title}</span>
                  <span className={`status-badge ${statusClass[r.status] || ''}`}>
                    {statusLabel[r.status] || r.status}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* Historial de transacciones */}
        <div className="dashboard-card">
          <div className="card-header">
            <h2>Transacciones Recientes</h2>
            <Link to="/transactions" className="link-more">Ver todas →</Link>
          </div>
          {recentTransactions.length === 0 ? (
            <p className="empty-state">No hay transacciones recientes.</p>
          ) : (
            <ul className="dashboard-list">
              {recentTransactions.map(t => {
                const isSender = t.sender_id === user?.id;
                return (
                  <li key={t.id}>
                    <span className="list-item-title">
                      {isSender ? `→ ${t.receiver_name || 'Sistema'}` : `← ${t.sender_name || 'Sistema'}`}
                    </span>
                    <span className={`credit-amount ${isSender ? 'credit-out' : 'credit-in'}`}>
                      {isSender ? '-' : '+'}{t.credits} créditos
                    </span>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
