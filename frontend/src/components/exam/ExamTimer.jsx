import React, { useEffect } from 'react';
import { MdTimer, MdHourglassTop } from 'react-icons/md';
import useExamStore from '../../store/examStore';
import './ExamComponents.css';

export default function ExamTimer({ onTimeUp }) {
  const { timeRemaining, timerStarted, tick } = useExamStore();

  useEffect(() => {
    // Don't start the interval until the timer is explicitly started
    if (!timerStarted) return;

    const interval = setInterval(() => {
      const state = useExamStore.getState();
      if (state.timeRemaining <= 0) {
        clearInterval(interval);
        onTimeUp && onTimeUp();
        return;
      }
      state.tick();
    }, 1000);
    return () => clearInterval(interval);
  }, [timerStarted]);

  const safeRemaining = Number(timeRemaining) || 0;
  const minutes = Math.floor(safeRemaining / 60);
  const seconds = safeRemaining % 60;

  // Show waiting state when timer hasn't started yet
  if (!timerStarted) {
    return (
      <div className="exam-timer waiting">
        <MdHourglassTop className="timer-icon spinning" />
        <span className="timer-value">
          {String(minutes).padStart(2, '0')}:{String(seconds).padStart(2, '0')}
        </span>
        <span className="timer-waiting-label">Waiting...</span>
      </div>
    );
  }

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
