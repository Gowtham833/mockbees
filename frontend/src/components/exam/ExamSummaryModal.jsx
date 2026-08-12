import React from 'react';
import Modal from '../common/Modal';
import Button from '../common/Button';
import useExamStore from '../../store/examStore';
import './ExamComponents.css';

export default function ExamSummaryModal({ isOpen, onClose, onConfirm, loading }) {
  const { questions, answers, markedForReview } = useExamStore();
  const answered = questions.filter(q => answers[q.id]).length;
  const unanswered = questions.length - answered;
  const marked = markedForReview.length;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Submit Test">
      {unanswered > 0 && (
        <div className="summary-warning">⚠️ You have {unanswered} unanswered question{unanswered > 1 ? 's' : ''}!</div>
      )}
      <div className="summary-stats">
        <div className="summary-stat answered"><div className="summary-stat-value">{answered}</div><div className="summary-stat-label">Answered</div></div>
        <div className="summary-stat unanswered"><div className="summary-stat-value">{unanswered}</div><div className="summary-stat-label">Unanswered</div></div>
        <div className="summary-stat marked"><div className="summary-stat-value">{marked}</div><div className="summary-stat-label">Marked for Review</div></div>
        <div className="summary-stat total"><div className="summary-stat-value">{questions.length}</div><div className="summary-stat-label">Total Questions</div></div>
      </div>
      <div className="summary-actions">
        <Button variant="ghost" onClick={onClose}>Go Back</Button>
        <Button variant="danger" onClick={onConfirm} loading={loading}>Confirm Submit</Button>
      </div>
    </Modal>
  );
}
