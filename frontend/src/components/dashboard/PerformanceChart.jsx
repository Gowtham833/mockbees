import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Card from '../common/Card';
import './Dashboard.css';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: 'var(--bg-secondary)', border: '1px solid var(--glass-border)', borderRadius: 8, padding: '10px 14px' }}>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>{label}</p>
      <p style={{ color: 'var(--accent)', fontWeight: 700 }}>{payload[0].value}%</p>
    </div>
  );
};

export default function PerformanceChart({ data = [] }) {
  if (!data.length) return (
    <Card><div className="chart-title">Performance Trend</div><div className="empty-state"><div className="empty-state-text">Take some tests to see your progress!</div></div></Card>
  );
  return (
    <Card>
      <div className="chart-title">Performance Trend</div>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={250}>
          <AreaChart data={data}>
            <defs>
              <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="date" stroke="#6b6b80" fontSize={12} />
            <YAxis stroke="#6b6b80" fontSize={12} domain={[0, 100]} />
            <Tooltip content={<CustomTooltip />} />
            <Area type="monotone" dataKey="score" stroke="#f59e0b" fill="url(#scoreGradient)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}
