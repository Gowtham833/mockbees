import React from 'react';
import { MdQuiz, MdTrendingUp, MdCheckCircle } from 'react-icons/md';
import './Dashboard.css';

export default function StatsOverview({ stats }) {
  const items = [
    { icon: <MdQuiz />, label: 'Tests Taken', value: stats?.total_tests || 0, color: 'blue' },
    { icon: <MdTrendingUp />, label: 'Avg Score', value: `${Math.round(stats?.average_score || 0)}%`, color: 'green' },
    { icon: '🔥', label: 'Current Streak', value: stats?.current_streak || 0, color: 'orange' },
    { icon: <MdCheckCircle />, label: 'Questions Done', value: stats?.total_questions || 0, color: 'purple' },
  ];
  return (
    <div className="stats-grid">
      {items.map((item, i) => (
        <div className="stat-card" key={i}>
          <div className={`stat-icon ${item.color}`}>{item.icon}</div>
          <div>
            <div className="stat-value">{item.value}</div>
            <div className="stat-label">{item.label}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
