import React, { useState } from 'react';
import Card from '../common/Card';
import { MdExpandMore, MdExpandLess } from 'react-icons/md';
import './Results.css';

export default function QuestionReview({ questions = [], answers = {} }) {
  const [expanded, setExpanded] = useState({});
  const toggle = (id) => setExpanded(prev => ({ ...prev, [id]: !prev[id] }));

  return (
    <div>
      {questions.map((q, i) => {
        const userAnswer = answers[q.id];
        const options = [
          { label: 'A', text: q.option_a },
          { label: 'B', text: q.option_b },
          { label: 'C', text: q.option_c },
          { label: 'D', text: q.option_d },
        ];
        return (
          <Card key={q.id} className="review-question">
            <div className="review-q-header">
              <span className="review-q-num">Q{i + 1}</span>
              <span className="question-subject">{q.subject}</span>
            </div>
            <p className="review-q-text">{q.question_text || q.question}</p>
            {options.map(opt => {
              let cls = 'neutral';
              if (opt.label === q.correct_answer) cls = 'correct';
              else if (opt.label === userAnswer && opt.label !== q.correct_answer) cls = 'wrong';
              return (
                <div key={opt.label} className={`review-option ${cls}`}>
                  <strong>{opt.label}.</strong> {opt.text}
                </div>
              );
            })}
            <button className="review-explanation-toggle" onClick={() => toggle(q.id)}>
              {expanded[q.id] ? <MdExpandLess /> : <MdExpandMore />}
              {expanded[q.id] ? 'Hide' : 'Show'} Explanation
            </button>
            {expanded[q.id] && <div className="review-explanation">{q.explanation}</div>}
          </Card>
        );
      })}
    </div>
  );
}
