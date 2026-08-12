import React from 'react';
import { NavLink } from 'react-router-dom';
import { MdDashboard, MdQuiz, MdBarChart, MdBookmark, MdPerson } from 'react-icons/md';
import { useUiStore } from '../../store/uiStore';
import './Sidebar.css';

const Sidebar = () => {
  const { sidebarOpen } = useUiStore();

  const navItems = [
    { path: '/dashboard', name: 'Dashboard', icon: <MdDashboard size={22} /> },
    { path: '/exams', name: 'Exams', icon: <MdQuiz size={22} /> },
    { path: '/analytics', name: 'Analytics', icon: <MdBarChart size={22} /> },
    { path: '/profile', name: 'Profile', icon: <MdPerson size={22} /> },
  ];

  return (
    <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
      <div className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <div className="nav-icon">{item.icon}</div>
            <span className="nav-label">{item.name}</span>
          </NavLink>
        ))}
      </div>
      
      <div className="sidebar-footer">
        <div className="pro-card glass-card">
          <div className="pro-icon">👑</div>
          <h4>Go Pro</h4>
          <p>Get access to all premium mock tests.</p>
          <button className="btn-primary btn-sm">Upgrade</button>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
