import React from 'react';
import Card from '../common/Card';
import './Results.css';

export default function ResultSummary({ result }) {
  if (!result) return null;
  const pct = result.max_score > 0 ? Math.round((result.score / result.max_score) * 100) : 0;
  const circumference = 2 * Math.PI * 65;
  const offset = circumference - (pct / 100) * circumference;
  const color = pct >= 70 ? 'var(--success)' : pct >= 40 ? 'var(--warning)' : 'var(--error)';
  return (
    <Card>
      <div className="result-hero">
        <div className="result-score-circle">
          <svg width="160" height="160">
            <circle className="bg" cx="80" cy="80" r="65" fill="none" strokeWidth="8" />
            <circle className="progress" cx="80" cy="80" r="65" fill="none" stroke={color} strokeWidth="8" strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={offset} />
          </svg>
          <div className="result-score-text">
            <div className="result-score-value">{pct}%</div>
            <div className="result-score-label">{result.score}/{result.max_score}</div>
          </div>
        </div>
        <div className="result-stats">
          <div className="result-stat"><div className="result-stat-value correct">{result.correct_answers}</div><div className="result-stat-label">Correct</div></div>
          <div className="result-stat"><div className="result-stat-value incorrect">{result.incorrect_answers}</div><div className="result-stat-label">Incorrect</div></div>
          <div className="result-stat"><div className="result-stat-value unanswered">{result.unanswered}</div><div className="result-stat-label">Unanswered</div></div>
        </div>
      </div>
    </Card>
  );
}
