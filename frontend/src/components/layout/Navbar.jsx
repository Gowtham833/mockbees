import React from 'react';
import { MdMenu, MdNotifications, MdSearch } from 'react-icons/md';
import { useUiStore } from '../../store/uiStore';
import { useAuthStore } from '../../store/authStore';
import './Navbar.css';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const { toggleSidebar } = useUiStore();
  const { user, logout } = useAuthStore();

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <button className="icon-btn mobile-menu-btn" onClick={toggleSidebar}>
          <MdMenu size={24} />
        </button>
        <Link to="/dashboard" className="brand-logo">
          <span className="brand-icon">🐝</span>
          <span className="brand-text">MockBees</span>
        </Link>
      </div>

      <div className="navbar-center">
        <div className="search-bar">
          <MdSearch className="search-icon" size={20} />
          <input type="text" placeholder="Search exams, topics..." />
        </div>
      </div>

      <div className="navbar-right">
        <button className="icon-btn notification-btn">
          <MdNotifications size={24} />
          <span className="badge">3</span>
        </button>
        
        <div className="user-profile">
          <div className="avatar">
            {user?.name?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div className="user-dropdown">
            <div className="dropdown-header">
              <strong>{user?.name || 'User'}</strong>
              <span>{user?.email || 'user@example.com'}</span>
            </div>
            <Link to="/profile" className="dropdown-item">Profile</Link>
            <button onClick={logout} className="dropdown-item text-danger">Logout</button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
