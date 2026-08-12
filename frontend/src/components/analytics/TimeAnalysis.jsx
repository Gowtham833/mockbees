import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Card from '../common/Card';
import './Analytics.css';

export default function TimeAnalysis({ data = [] }) {
  if (!data.length) return null;
  return (
    <Card>
      <div className="chart-title">Time per Subject</div>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis type="number" stroke="#6b6b80" fontSize={12} />
          <YAxis dataKey="subject" type="category" stroke="#6b6b80" fontSize={12} width={120} />
          <Tooltip contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--glass-border)', borderRadius: 8 }} />
          <Bar dataKey="time" fill="#667eea" radius={[0, 4, 4, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}
