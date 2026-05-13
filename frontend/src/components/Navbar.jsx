import React, { useContext, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { getUnreadMessageCount } from '../services/api';
import './Navbar.css';


const Navbar = () => {
  const { isAuthenticated, user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [unreadCount, setUnreadCount] = useState(0);
  const [unreadFrom, setUnreadFrom] = useState([]);
  const [pendingRequests, setPendingRequests] = useState([]);

  useEffect(() => {
    if (!isAuthenticated) {
      setUnreadCount(0);
      setUnreadFrom([]);
      setPendingRequests([]);
      return;
    }

    const fetchUnread = async () => {
      try {
        const data = await getUnreadMessageCount();
        setUnreadCount(data.unread || 0);
        setUnreadFrom(data.from || []);
        setPendingRequests(data.pending_requests || []);
      } catch {
        // silencioso
      }
    };

    fetchUnread();
    const interval = setInterval(fetchUnread, 30_000);
    return () => clearInterval(interval);
  }, [isAuthenticated]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <h2><Link to="/">Time Bank</Link></h2>
      <div className="nav-links">
        {isAuthenticated ? (
          <>
            <Link to="/dashboard">Panel</Link>
            <Link to="/services">Servicios</Link>
            <div className="nav-link-wrapper">
              <Link to="/requests" className="nav-link-with-badge">
                Solicitudes
                {(unreadCount + pendingRequests.length) > 0 && (
                  <span className="nav-badge">
                    {(unreadCount + pendingRequests.length) > 99 ? '99+' : (unreadCount + pendingRequests.length)}
                  </span>
                )}
              </Link>
              {(unreadFrom.length > 0 || pendingRequests.length > 0) && (
                <div className="unread-popover">
                  {pendingRequests.length > 0 && (
                    <>
                      <div className="unread-popover-title">Nuevas solicitudes</div>
                      {pendingRequests.map((item, i) => (
                        <Link
                          key={i}
                          to="/requests"
                          state={{ openRequestId: item.request_id }}
                          className="unread-popover-item"
                        >
                          <span className="unread-popover-name">
                            <span className="unread-popover-meta">{item.requester_name}</span>
                            {item.service_title}
                          </span>
                          <span className="unread-popover-count unread-popover-count--new">nueva</span>
                        </Link>
                      ))}
                    </>
                  )}
                  {pendingRequests.length > 0 && unreadFrom.length > 0 && (
                    <div className="unread-popover-divider" />
                  )}
                  {unreadFrom.length > 0 && (
                    <>
                      <div className="unread-popover-title">Mensajes sin leer</div>
                      {unreadFrom.map((item, i) => (
                        <Link
                          key={i}
                          to="/requests"
                          state={{ openRequestId: item.request_id }}
                          className="unread-popover-item"
                        >
                          <span className="unread-popover-name">{item.name}</span>
                          <span className="unread-popover-count">{item.count} msg</span>
                        </Link>
                      ))}
                    </>
                  )}
                </div>
              )}
            </div>
            <Link to="/transactions">Transacciones</Link>
            <Link to="/buy-credits" className="nav-buy-credits">Comprar créditos</Link>
            {user?.role === 'admin' && <Link to="/admin">Admin</Link>}
            <span className="user-greeting">Hola, {user?.name}</span>
            <button onClick={handleLogout} className="btn-logout">Cerrar Sesión</button>
          </>
        ) : (
          <>
            <Link to="/login">Iniciar Sesión</Link>
            <Link to="/register" className="btn-register">Registrarse</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
