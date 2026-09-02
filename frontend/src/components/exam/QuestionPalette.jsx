import React from 'react';
import useExamStore from '../../store/examStore';
import './ExamComponents.css';

export default function QuestionPalette() {
  const { questions, answers, currentQuestionIndex, markedForReview, goToQuestion, currentTest } = useExamStore();

  const getStatus = (q, i) => {
    if (i === currentQuestionIndex) return 'current';
    if (q && markedForReview.includes(q.id)) return 'marked';
    if (q && answers[q.id]) return 'answered';
    return '';
  };

  const totalQ = currentTest?.total_questions || questions.length || 0;
  const examSubjects = currentTest?.exam?.subjects || [];

  // Build sections based on actual question subjects
  const sections = {};
  const subjectOrder = [];

  // Initialize sections from exam subject definitions (preserving defined order)
  if (examSubjects.length > 0) {
    examSubjects.forEach((subj) => {
      sections[subj.name] = [];
      subjectOrder.push(subj.name);
    });
  }

  // Group questions by their actual subject field
  questions.forEach((q, i) => {
    const subj = q.subject || 'General';
    if (!sections[subj]) {
      sections[subj] = [];
      subjectOrder.push(subj);
    }
    sections[subj].push({ index: i, question: q });
  });

  // If there are placeholder slots for questions still being generated,
  // add them to a "Generating..." section
  if (questions.length < totalQ) {
    const pendingCount = totalQ - questions.length;
    if (pendingCount > 0) {
      const pendingKey = '⏳ Generating...';
      sections[pendingKey] = [];
      subjectOrder.push(pendingKey);
      for (let i = questions.length; i < totalQ; i++) {
        sections[pendingKey].push({ index: i, question: null });
      }
    }
  }

  // Remove empty sections from the order
  const filteredOrder = subjectOrder.filter(subj => sections[subj] && sections[subj].length > 0);

  return (
    <div className="palette-container glass-card">
      <div className="palette-title">Question Palette</div>

      {/* Section quick-jump buttons */}
      <div className="palette-sections">
        {filteredOrder.map((subj) => {
          const firstReady = sections[subj].find(item => item.question !== null);
          const isGeneratingSection = subj === '⏳ Generating...';

          return (
            <div key={subj} className="palette-section">
              <button
                className={`palette-section-btn ${isGeneratingSection ? 'generating-section' : ''}`}
                onClick={() => firstReady && goToQuestion(firstReady.index)}
                disabled={!firstReady}
              >
                <span className="section-name">{subj}</span>
                <span className="section-count">{sections[subj].length}</span>
              </button>
            </div>
          );
        })}
      </div>

      {/* Question grid per section */}
      <div className="palette-sections-content" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {filteredOrder.map((subj) => {
          const items = sections[subj];
          if (!items || items.length === 0) return null;

          return (
            <div key={`grid-${subj}`} className="palette-section-group">
              <h4 style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#a0a0b0' }}>{subj}</h4>
              <div className="palette-grid">
                {items.map(({ index: i, question: q }) => {
                  const isGenerating = !q;
                  
                  return (
                    <button
                      key={q?.id || `placeholder-${i}`}
                      className={`palette-btn ${isGenerating ? 'generating' : getStatus(q, i)}`}
                      onClick={() => !isGenerating && goToQuestion(i)}
                      disabled={isGenerating}
                      title={isGenerating ? 'Question is being generated...' : `Question ${i + 1}`}
                    >
                      {i + 1}
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      <div className="palette-legend" style={{ marginTop: '20px' }}>
        <div className="legend-item"><span className="legend-dot answered" /> Answered</div>
        <div className="legend-item"><span className="legend-dot unanswered" /> Not Visited</div>
        <div className="legend-item"><span className="legend-dot marked" /> Marked</div>
        <div className="legend-item"><span className="legend-dot current" /> Current</div>
        {questions.length < totalQ && (
          <div className="legend-item"><span className="legend-dot generating" /> Generating</div>
        )}
      </div>
    </div>
  );
}
