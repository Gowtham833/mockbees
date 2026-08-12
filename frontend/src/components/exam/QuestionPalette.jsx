import React from 'react';
import useExamStore from '../../store/examStore';
import './ExamComponents.css';

export default function QuestionPalette() {
  const { questions, answers, currentQuestionIndex, markedForReview, goToQuestion, currentTest } = useExamStore();

  const getStatus = (q, i) => {
    if (i === currentQuestionIndex) return 'current';
    if (markedForReview.includes(q.id)) return 'marked';
    if (answers[q.id]) return 'answered';
    return '';
  };

  const sectionOrder = currentTest?.subjects?.map((s) => s.name) || [];
  const sections = {};

  questions.forEach((q, i) => {
    const subj = q.subject || 'General';
    if (!sections[subj]) sections[subj] = [];
    sections[subj].push(i);
  });

  sectionOrder.forEach((name) => {
    if (!sections[name]) sections[name] = [];
  });

  // Include any actual question subjects not present in the exam subjects list
  Object.keys(sections).forEach((name) => {
    if (!sectionOrder.includes(name)) {
      sectionOrder.push(name);
    }
  });

  return (
    <div className="palette-container glass-card">
      <div className="palette-title">Question Palette</div>

      <div className="palette-sections">
        {sectionOrder.map((subj) => (
          <div key={subj} className="palette-section">
            <button
              className="palette-section-btn"
              onClick={() => sections[subj]?.length > 0 && goToQuestion(sections[subj][0])}
              disabled={sections[subj]?.length === 0}
            >
              <span className="section-name">{subj}</span>
              <span className="section-count">{sections[subj]?.length || 0}</span>
            </button>
          </div>
        ))}
      </div>

      <div className="palette-grid">
        {questions.map((q, i) => (
          <button
            key={q.id}
            className={`palette-btn ${getStatus(q, i)}`}
            onClick={() => goToQuestion(i)}
          >
            {i + 1}
          </button>
        ))}
      </div>
      <div className="palette-legend">
        <div className="legend-item"><span className="legend-dot answered" /> Answered</div>
        <div className="legend-item"><span className="legend-dot unanswered" /> Not Visited</div>
        <div className="legend-item"><span className="legend-dot marked" /> Marked</div>
        <div className="legend-item"><span className="legend-dot current" /> Current</div>
      </div>
    </div>
  );
}
