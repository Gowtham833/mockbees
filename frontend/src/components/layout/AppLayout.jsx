import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import { useUiStore } from '../../store/uiStore';
import './AppLayout.css';

const AppLayout = () => {
  const { sidebarOpen } = useUiStore();

  return (
    <div className={`app-layout ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
      <Navbar />
      <Sidebar />
      <main className="app-main-content">
        <div className="content-container">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default AppLayout;
