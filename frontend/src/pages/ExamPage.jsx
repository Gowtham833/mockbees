import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ExamHeader from '../components/exam/ExamHeader';
import QuestionCard from '../components/exam/QuestionCard';
import QuestionPalette from '../components/exam/QuestionPalette';
import ExamSummaryModal from '../components/exam/ExamSummaryModal';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import useExamStore from '../store/examStore';
import { examService } from '../services/examService';
import toast from 'react-hot-toast';
import './ExamPage.css';

export default function ExamPage() {
  const { testId } = useParams();
  const navigate = useNavigate();
  const { questions, currentQuestionIndex, answers, nextQuestion, prevQuestion, clearAnswer, setTest, resetExam, timeRemaining } = useExamStore();
  const [showSummary, setShowSummary] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (questions.length > 0 && useExamStore.getState().currentTest?.id == testId) {
      setLoading(false);
      return;
    }
    examService.getTestAttempt(testId).then(r => {
      const data = r.data;
      setTest(data, data.questions || []);
      setLoading(false);
    }).catch(() => { toast.error('Failed to load test'); navigate('/dashboard'); });
  }, [testId]);

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const answerList = Object.entries(answers).map(([qId, ans]) => ({ question_id: parseInt(qId), selected_answer: ans, time_spent_seconds: 0 }));
      await examService.submitTest(testId, { answers: answerList, time_taken_seconds: useExamStore.getState().currentTest?.duration_seconds - timeRemaining });
      resetExam();
      toast.success('Test submitted!');
      navigate(`/results/${testId}`);
    } catch (e) {
      toast.error('Submit failed');
      setSubmitting(false);
    }
  };

  const handleTimeUp = () => { toast('⏰ Time is up!'); handleSubmit(); };

  if (loading) return <LoadingSpinner text="Loading test..." />;
  const currentQ = questions[currentQuestionIndex];
  if (!currentQ) return <LoadingSpinner text="Loading..." />;

  return (
    <div className="exam-page">
      <ExamHeader examName={useExamStore.getState().examName || 'Mock Test'} onSubmit={() => setShowSummary(true)} onTimeUp={handleTimeUp} />
      <div className="exam-body">
        <div className="exam-main">
          <QuestionCard question={currentQ} index={currentQuestionIndex} />
        </div>
        <div className="exam-sidebar">
          <QuestionPalette />
        </div>
      </div>
      <div className="exam-nav">
        <Button variant="secondary" onClick={prevQuestion} disabled={currentQuestionIndex === 0}>Previous</Button>
        <Button variant="ghost" onClick={() => clearAnswer(currentQ.id)}>Clear</Button>
        <Button variant="secondary" onClick={nextQuestion} disabled={currentQuestionIndex === questions.length - 1}>Next</Button>
      </div>
      <ExamSummaryModal isOpen={showSummary} onClose={() => setShowSummary(false)} onConfirm={handleSubmit} loading={submitting} />
    </div>
  );
}
