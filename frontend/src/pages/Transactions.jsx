import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import * as api from '../services/api';
import './Transactions.css';

const TYPE_LABELS = {
  transfer: 'Transferencia',
  purchase: 'Pago de servicio',
  refund: 'Reembolso',
  system: 'Sistema'
};

const Transactions = () => {
  const { user } = useContext(AuthContext);

  const [transactions, setTransactions] = useState([]);
  const [balance, setBalance] = useState(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const perPage = 15;

  const [typeFilter, setTypeFilter] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Modal transferir créditos
  const [showTransferModal, setShowTransferModal] = useState(false);
  const [transferForm, setTransferForm] = useState({ receiver_id: '', credits: '', type: 'transfer' });
  const [transferError, setTransferError] = useState(null);
  const [transferring, setTransferring] = useState(false);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.getTransactions({
        type: typeFilter || undefined,
        page,
        per_page: perPage
      });
      setTransactions(data.items || []);
      setTotal(data.total || 0);
      if (data.balance !== undefined) {
        setBalance(data.balance);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, [typeFilter, page]);

  const handleTransferChange = (e) => {
    setTransferForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleTransferSubmit = async (e) => {
    e.preventDefault();
    const credits = parseInt(transferForm.credits);
    if (!transferForm.receiver_id || isNaN(credits) || credits <= 0) {
      setTransferError('ID de receptor y créditos (> 0) son obligatorios.');
      return;
    }
    try {
      setTransferring(true);
      setTransferError(null);
      await api.transferCredits({
        receiver_id: parseInt(transferForm.receiver_id),
        credits,
        type: 'transfer'
      });
      setShowTransferModal(false);
      setTransferForm({ receiver_id: '', credits: '', type: 'transfer' });
      fetchTransactions();
    } catch (err) {
      setTransferError(err.message);
    } finally {
      setTransferring(false);
    }
  };

  const totalPages = Math.ceil(total / perPage);

  const formatDate = (dateStr) => {
    if (!dateStr) return '—';
    return new Date(dateStr).toLocaleString('es-ES', { dateStyle: 'medium', timeStyle: 'short' });
  };

  return (
    <div className="transactions-page">
      <div className="transactions-header">
        <div>
          <h1>Historial de Transacciones</h1>
          <p className="subtitle">Registro de todos tus movimientos de créditos</p>
        </div>
        <button className="btn-primary" onClick={() => { setShowTransferModal(true); setTransferError(null); }}>
          Transferir créditos
        </button>
      </div>

      {/* Balance */}
      {balance !== null && (
        <div className="balance-banner">
          <span className="balance-banner-label">Tu saldo actual</span>
          <span className="balance-banner-amount">{balance} créditos</span>
        </div>
      )}

      {/* Filtros */}
      <div className="transactions-filters">
        <select
          value={typeFilter}
          onChange={e => { setTypeFilter(e.target.value); setPage(1); }}
          className="filter-select"
        >
          <option value="">Todos los tipos</option>
          {Object.entries(TYPE_LABELS).map(([val, label]) => (
            <option key={val} value={val}>{label}</option>
          ))}
        </select>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {loading ? (
        <div className="loading-state">Cargando transacciones...</div>
      ) : transactions.length === 0 ? (
        <div className="empty-state-block">
          <p>No hay transacciones que mostrar.</p>
        </div>
      ) : (
        <>
          <div className="transactions-table-wrapper">
            <table className="transactions-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Tipo</th>
                  <th>De</th>
                  <th>Para</th>
                  <th>Créditos</th>
                  <th>Fecha</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map(tx => {
                  const isSender = tx.sender_id === user?.id;
                  return (
                    <tr key={tx.id}>
                      <td className="tx-id">#{tx.id}</td>
                      <td>
                        <span className={`type-badge type-${tx.type}`}>
                          {TYPE_LABELS[tx.type] || tx.type}
                        </span>
                      </td>
                      <td>
                        <span className={tx.sender_id === user?.id ? 'me-label' : ''}>
                          {tx.sender_name || 'Sistema'}
                          {tx.sender_id === user?.id && ' (yo)'}
                        </span>
                      </td>
                      <td>
                        <span className={tx.receiver_id === user?.id ? 'me-label' : ''}>
                          {tx.receiver_name || 'Sistema'}
                          {tx.receiver_id === user?.id && ' (yo)'}
                        </span>
                      </td>
                      <td>
                        <span className={`credit-chip ${isSender ? 'credit-out' : 'credit-in'}`}>
                          {isSender ? '-' : '+'}{tx.credits}
                        </span>
                      </td>
                      <td className="tx-date">{formatDate(tx.created_at)}</td>
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
              <span className="page-info">Página {page} de {totalPages} ({total} transacciones)</span>
              <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)} className="btn-outline btn-sm">
                Siguiente →
              </button>
            </div>
          )}
        </>
      )}

      {/* Modal transferir */}
      {showTransferModal && (
        <div className="modal-overlay" onClick={() => setShowTransferModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Transferir créditos</h2>
              <button className="modal-close" onClick={() => setShowTransferModal(false)}>✕</button>
            </div>
            <form onSubmit={handleTransferSubmit} className="modal-form">
              {balance !== null && (
                <p className="current-balance">Saldo disponible: <strong>{balance} créditos</strong></p>
              )}
              {transferError && <div className="alert alert-error">{transferError}</div>}
              <div className="form-group">
                <label>ID del usuario receptor</label>
                <input
                  type="number"
                  name="receiver_id"
                  value={transferForm.receiver_id}
                  onChange={handleTransferChange}
                  placeholder="Ej: 5"
                  min="1"
                  required
                />
              </div>
              <div className="form-group">
                <label>Créditos a transferir</label>
                <input
                  type="number"
                  name="credits"
                  value={transferForm.credits}
                  onChange={handleTransferChange}
                  placeholder="Ej: 2"
                  min="1"
                  max={balance ?? undefined}
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-outline" onClick={() => setShowTransferModal(false)}>
                  Cancelar
                </button>
                <button type="submit" className="btn-primary" disabled={transferring}>
                  {transferring ? 'Transfiriendo...' : 'Transferir'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Transactions;
