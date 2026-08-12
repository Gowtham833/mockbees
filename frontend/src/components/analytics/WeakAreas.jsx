import React from 'react';
import Card from '../common/Card';
import './Analytics.css';

export default function WeakAreas({ areas = [] }) {
  if (!areas.length) return (
    <Card><div className="chart-title">Areas for Improvement</div><div className="empty-state"><div className="empty-state-text">Take more tests to identify weak areas.</div></div></Card>
  );
  const getLevel = (acc) => acc < 40 ? 'low' : acc < 70 ? 'medium' : 'high';
  const getColor = (acc) => acc < 40 ? 'var(--error)' : acc < 70 ? 'var(--warning)' : 'var(--success)';
  return (
    <Card>
      <div className="chart-title">Areas for Improvement</div>
      <div className="weak-list">
        {areas.map((a, i) => (
          <div className="weak-item" key={i}>
            <div style={{ flex: 1 }}>
              <div className="weak-topic">{a.topic}</div>
              <div className="weak-bar"><div className="weak-bar-fill" style={{ width: `${a.accuracy}%`, background: getColor(a.accuracy) }} /></div>
            </div>
            <span className={`weak-accuracy ${getLevel(a.accuracy)}`}>{Math.round(a.accuracy)}%</span>
          </div>
        ))}
      </div>
    </Card>
  );
}
