import React from 'react';
import ExamTimer from './ExamTimer';
import Button from '../common/Button';
import './ExamComponents.css';

export default function ExamHeader({ examName, onSubmit, onTimeUp }) {
  return (
    <div className="exam-header">
      <div className="exam-header-title">🐝 {examName}</div>
      <ExamTimer onTimeUp={onTimeUp} />
      <div className="exam-header-actions">
        <Button variant="danger" size="sm" onClick={onSubmit}>Submit Test</Button>
      </div>
    </div>
  );
}
