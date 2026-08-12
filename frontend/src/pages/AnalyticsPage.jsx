import React, { useEffect, useState } from 'react';
import StatsOverview from '../components/dashboard/StatsOverview';
import PerformanceChart from '../components/dashboard/PerformanceChart';
import TopicAnalysis from '../components/analytics/TopicAnalysis';
import WeakAreas from '../components/analytics/WeakAreas';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { analyticsService } from '../services/analyticsService';
import './AnalyticsPage.css';

export default function AnalyticsPage() {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [topics, setTopics] = useState([]);
  const [weak, setWeak] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      const [s, h, t, w] = await Promise.allSettled([
        analyticsService.getOverview(), analyticsService.getHistory(),
        analyticsService.getTopicPerformance(), analyticsService.getWeakAreas(),
      ]);
      if (s.status === 'fulfilled') setStats(s.value.data);
      if (h.status === 'fulfilled') setHistory(h.value.data || []);
      if (t.status === 'fulfilled') setTopics(t.value.data || []);
      if (w.status === 'fulfilled') setWeak(w.value.data || []);
      setLoading(false);
    };
    load();
  }, []);

  if (loading) return <LoadingSpinner text="Loading analytics..." />;

  return (
    <div className="analytics-page">
      <h1>Performance Analytics 📈</h1>
      <StatsOverview stats={stats} />
      <PerformanceChart data={history} />
      <div className="analytics-row">
        <TopicAnalysis data={topics} />
        <WeakAreas areas={weak} />
      </div>
    </div>
  );
}
