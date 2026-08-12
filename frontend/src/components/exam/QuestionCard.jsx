import React from 'react';
import { motion } from 'framer-motion';
import { MdBookmarkBorder, MdBookmark } from 'react-icons/md';
import useExamStore from '../../store/examStore';
import './ExamComponents.css';

export default function QuestionCard({ question, index }) {
  const { answers, setAnswer, markedForReview, toggleMarkForReview } = useExamStore();
  const selected = answers[question.id];
  const isMarked = markedForReview.includes(question.id);
  const options = [
    { label: 'A', text: question.option_a },
    { label: 'B', text: question.option_b },
    { label: 'C', text: question.option_c },
    { label: 'D', text: question.option_d },
  ];

  return (
    <motion.div
      className="question-card glass-card"
      key={question.id}
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="question-header">
        <span className="question-number">Question {index + 1}</span>
        <span className="question-subject">{question.subject}</span>
        {question.difficulty ? <span className={`question-difficulty difficulty-${question.difficulty.replace(/\s+/g, '-').toLowerCase()}`}>{question.difficulty}</span> : null}
      </div>
      <p className="question-text">{question.question_text || question.question}</p>
      <div className="options-list">
        {options.map((opt) => (
          <div
            key={opt.label}
            className={`option-item ${selected === opt.label ? 'selected' : ''}`}
            onClick={() => setAnswer(question.id, opt.label)}
          >
            <span className="option-label">{opt.label}</span>
            <span className="option-text">{opt.text}</span>
          </div>
        ))}
      </div>
      <button
        className={`mark-review-btn ${isMarked ? 'marked' : ''}`}
        onClick={() => toggleMarkForReview(question.id)}
      >
        {isMarked ? <MdBookmark /> : <MdBookmarkBorder />}
        {isMarked ? 'Marked for Review' : 'Mark for Review'}
      </button>
    </motion.div>
  );
}
