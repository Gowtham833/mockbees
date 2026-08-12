import React, { useEffect, useState } from 'react';
import StatsOverview from '../components/dashboard/StatsOverview';
import PerformanceChart from '../components/dashboard/PerformanceChart';
import QuickActions from '../components/dashboard/QuickActions';
import RecentAttempts from '../components/dashboard/RecentAttempts';
import LoadingSpinner from '../components/common/LoadingSpinner';
import useAuthStore from '../store/authStore';
import { analyticsService } from '../services/analyticsService';
import { examService } from '../services/examService';
import './DashboardPage.css';

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [s, h, c] = await Promise.allSettled([
          analyticsService.getOverview(),
          examService.getHistory(),
          analyticsService.getHistory(),
        ]);
        if (s.status === 'fulfilled') setStats(s.value.data);
        if (h.status === 'fulfilled') setHistory(h.value.data || []);
        if (c.status === 'fulfilled') setChartData(c.value.data || []);
      } catch (e) { console.error(e); }
      setLoading(false);
    };
    load();
  }, []);

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good Morning' : hour < 17 ? 'Good Afternoon' : 'Good Evening';

  if (loading) return <LoadingSpinner text="Loading dashboard..." />;

  return (
    <div className="dashboard">
      <div className="dashboard-welcome">
        <h1>{greeting}, {user?.name || 'Student'}! 👋</h1>
        <p>Here's your preparation overview</p>
      </div>
      <StatsOverview stats={stats} />
      <div className="dashboard-grid">
        <PerformanceChart data={chartData} />
        <QuickActions />
      </div>
      <RecentAttempts attempts={history} />
    </div>
  );
}
