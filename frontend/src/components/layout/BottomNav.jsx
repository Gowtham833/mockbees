import React from 'react';
import { NavLink } from 'react-router-dom';
import { FiHome, FiBookOpen, FiBarChart2, FiUser } from 'react-icons/fi';
import './BottomNav.css';

const BottomNav = () => {
  return (
    <div className="bottom-nav">
      <NavLink to="/dashboard" className={({ isActive }) => `bottom-nav-item ${isActive ? 'active' : ''}`}>
        <FiHome className="bottom-nav-icon" />
        <span className="bottom-nav-label">Home</span>
      </NavLink>
      <NavLink to="/exams" className={({ isActive }) => `bottom-nav-item ${isActive ? 'active' : ''}`}>
        <FiBookOpen className="bottom-nav-icon" />
        <span className="bottom-nav-label">Exams</span>
      </NavLink>
      <NavLink to="/analytics" className={({ isActive }) => `bottom-nav-item ${isActive ? 'active' : ''}`}>
        <FiBarChart2 className="bottom-nav-icon" />
        <span className="bottom-nav-label">Stats</span>
      </NavLink>
      <NavLink to="/profile" className={({ isActive }) => `bottom-nav-item ${isActive ? 'active' : ''}`}>
        <FiUser className="bottom-nav-icon" />
        <span className="bottom-nav-label">Profile</span>
      </NavLink>
    </div>
  );
};

export default BottomNav;
