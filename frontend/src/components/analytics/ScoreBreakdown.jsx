import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import Card from '../common/Card';
import './Analytics.css';

const COLORS = ['#10b981', '#f43f5e', '#6b6b80'];

export default function ScoreBreakdown({ correct = 0, incorrect = 0, unanswered = 0 }) {
  const data = [
    { name: 'Correct', value: correct },
    { name: 'Incorrect', value: incorrect },
    { name: 'Unanswered', value: unanswered },
  ].filter(d => d.value > 0);
  const total = correct + incorrect + unanswered;
  if (!total) return null;
  return (
    <Card>
      <div className="chart-title">Score Breakdown</div>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={3} dataKey="value">
            {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
          </Pie>
          <Tooltip contentStyle={{ background: 'var(--bg-secondary)', border: '1px solid var(--glass-border)', borderRadius: 8 }} />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 20, marginTop: 8 }}>
        {data.map((d, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            <div style={{ width: 10, height: 10, borderRadius: '50%', background: COLORS[i] }} />
            {d.name}: {d.value}
          </div>
        ))}
      </div>
    </Card>
  );
}
