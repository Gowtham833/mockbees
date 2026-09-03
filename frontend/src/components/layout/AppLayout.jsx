import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import BottomNav from './BottomNav';
import { useUiStore } from '../../store/uiStore';
import './AppLayout.css';

const AppLayout = () => {
  const { sidebarOpen, toggleSidebar } = useUiStore();

  return (
    <div className={`app-layout ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
      <Navbar />
      {/* Mobile backdrop - no longer needed since sidebar is hidden on mobile, but keep it for tablet logic just in case */}
      {sidebarOpen && (
        <div className="sidebar-backdrop" onClick={toggleSidebar}></div>
      )}
      <Sidebar />
      <BottomNav />
      <main className="app-main-content">
        <div className="content-container">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default AppLayout;
