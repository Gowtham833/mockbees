import React from 'react';
import { useNavigate } from 'react-router-dom';
import { format } from 'date-fns';
import Card from '../common/Card';
import './Dashboard.css';

export default function RecentAttempts({ attempts = [] }) {
  const navigate = useNavigate();
  if (!attempts.length) return (
    <Card><div className="empty-state"><div className="empty-state-icon">📋</div><div className="empty-state-text">No tests taken yet. Start your first mock test!</div></div></Card>
  );
  return (
    <Card>
      <div className="chart-title">Recent Attempts</div>
      <div style={{ overflowX: 'auto' }}>
        <table className="recent-table">
          <thead><tr><th>Exam</th><th>Score</th><th>Accuracy</th><th>Date</th><th>Status</th><th></th></tr></thead>
          <tbody>
            {attempts.map((a) => (
              <tr key={a.id}>
                <td>{a.exam_name || 'Mock Test'}</td>
                <td>{a.score}/{a.max_score}</td>
                <td>{Math.round(a.accuracy || 0)}%</td>
                <td>{a.completed_at ? format(new Date(a.completed_at), 'MMM d, yyyy') : '-'}</td>
                <td><span className={`status-badge ${a.status}`}>{a.status === 'in_progress' ? 'In Progress' : a.status === 'completed' ? 'Completed' : 'Abandoned'}</span></td>
                <td><button className="btn btn-ghost btn-sm" onClick={() => navigate(`/results/${a.id}`)}>View</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
