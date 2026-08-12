import React from 'react';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import Card from '../common/Card';
import './Analytics.css';

export default function TopicAnalysis({ data = [] }) {
  if (!data.length) return null;
  return (
    <Card>
      <div className="chart-title">Topic Performance</div>
      <ResponsiveContainer width="100%" height={300}>
        <RadarChart data={data}>
          <PolarGrid stroke="rgba(255,255,255,0.1)" />
          <PolarAngleAxis dataKey="topic" tick={{ fill: '#a0a0b8', fontSize: 11 }} />
          <PolarRadiusAxis tick={{ fill: '#6b6b80', fontSize: 10 }} domain={[0, 100]} />
          <Radar name="Accuracy" dataKey="accuracy" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.2} strokeWidth={2} />
        </RadarChart>
      </ResponsiveContainer>
    </Card>
  );
}
