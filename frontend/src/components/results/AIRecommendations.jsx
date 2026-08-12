import React from 'react';
import Card from '../common/Card';
import './Results.css';

export default function AIRecommendations({ weakAreas = [], score = 0 }) {
  const recommendations = [
    { icon: '🎯', title: 'Focus Areas', desc: weakAreas.length ? `Prioritize: ${weakAreas.slice(0, 3).map(w => w.topic || w).join(', ')}` : 'Great job! Keep practicing across all subjects.' },
    { icon: '📚', title: 'Study Strategy', desc: score >= 70 ? 'Focus on advanced concepts and time management.' : score >= 40 ? 'Review fundamentals and practice more questions daily.' : 'Start with basics. Focus on understanding core concepts first.' },
    { icon: '⏰', title: 'Time Management', desc: 'Practice with timed tests to improve speed. Aim to spend 45-60 seconds per question.' },
    { icon: '🔄', title: 'Practice Plan', desc: 'Take at least 2 mock tests per week. Review all incorrect answers thoroughly.' },
  ];
  return (
    <div className="recommendations-grid">
      {recommendations.map((r, i) => (
        <Card key={i} className="rec-card">
          <div className="rec-icon">{r.icon}</div>
          <div className="rec-title">{r.title}</div>
          <div className="rec-desc">{r.desc}</div>
        </Card>
      ))}
    </div>
  );
}
