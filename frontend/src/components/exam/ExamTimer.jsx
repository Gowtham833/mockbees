import React, { useEffect } from 'react';
import { MdTimer } from 'react-icons/md';
import useExamStore from '../../store/examStore';
import './ExamComponents.css';

export default function ExamTimer({ onTimeUp }) {
  const { timeRemaining, tick } = useExamStore();

  useEffect(() => {
    const interval = setInterval(() => {
      const remaining = useExamStore.getState().timeRemaining;
      if (remaining <= 0) { clearInterval(interval); onTimeUp && onTimeUp(); return; }
      tick();
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const safeRemaining = Number(timeRemaining) || 0;
  const minutes = Math.floor(safeRemaining / 60);
  const seconds = safeRemaining % 60;
  const status = safeRemaining <= 60 ? 'danger' : safeRemaining <= 300 ? 'warning' : '';

  return (
    <div className={`exam-timer ${status}`}>
      <MdTimer className="timer-icon" />
      <span className="timer-value">
        {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
      </span>
    </div>
  );
}
