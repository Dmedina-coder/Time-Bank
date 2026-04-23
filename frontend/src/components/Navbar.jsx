import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

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
            <Link to="/requests">Solicitudes</Link>
            <Link to="/transactions">Transacciones</Link>
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
