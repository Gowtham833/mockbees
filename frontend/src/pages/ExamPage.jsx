import React, { useEffect, useState, useRef } from 'react';
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
  const intervalRef = useRef(null);

  const generationStatus = useExamStore((s) => s.currentTest?.generation_status);
  const totalQuestions = useExamStore((s) => s.currentTest?.total_questions || 0);
  const isGenerating = generationStatus === 'PENDING' || generationStatus === 'GENERATING';

  useEffect(() => {
    const fetchTest = async () => {
      try {
        const r = await examService.getTestAttempt(testId);
        const data = r.data;
        useExamStore.getState().setTest(data, data.questions || []);
        setLoading(false);
        
        // If already READY, start the timer immediately
        if (data.generation_status === 'READY') {
          useExamStore.getState().startTimer();
        }
        
        // If still generating, set up polling
        if (data.generation_status === 'PENDING' || data.generation_status === 'GENERATING') {
          intervalRef.current = setInterval(async () => {
            try {
              const res = await examService.getTestAttempt(testId);
              const newData = res.data;
              useExamStore.getState().mergeQuestions(newData.questions || []);
              useExamStore.getState().updateTestStatus({
                generation_status: newData.generation_status,
                error_message: newData.error_message
              });
              
              if (newData.generation_status === 'READY' || newData.generation_status === 'FAILED') {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
                if (newData.generation_status === 'FAILED') {
                  toast.error(`Generation failed: ${newData.error_message}`);
                } else {
                  toast.success('All questions generated! Your timer starts now. Good luck! 🐝');
                  useExamStore.getState().startTimer();
                }
              }
            } catch (err) {
              console.error('Polling error', err);
            }
          }, 3000);
        }
      } catch (e) {
        toast.error('Failed to load test');
        navigate('/dashboard');
      }
    };
    
    // Check if we already have state for this test (e.g., page refresh)
    if (questions.length > 0 && useExamStore.getState().currentTest?.id == testId) {
      setLoading(false);
      const testStatus = useExamStore.getState().currentTest?.generation_status;
      if (testStatus === 'PENDING' || testStatus === 'GENERATING') {
        fetchTest();
      } else if (testStatus === 'READY' && !useExamStore.getState().timerStarted) {
        // Resume timer if test is ready but timer wasn't started (edge case)
        useExamStore.getState().startTimer();
      }
    } else {
      fetchTest();
    }
    
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
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

  return (
    <div className="exam-page">
      <ExamHeader examName={useExamStore.getState().examName || 'Mock Test'} onSubmit={() => setShowSummary(true)} onTimeUp={handleTimeUp} />
      
      {/* Generation progress banner */}
      {isGenerating && (
        <div className="exam-generating-banner">
          <div className="generating-banner-content">
            <div className="generating-spinner-wrapper">
              <LoadingSpinner size={24} />
            </div>
            <div className="generating-banner-text">
              <strong>🐝 AI is generating your questions...</strong>
              <span className="generating-progress">
                {questions.length} of {totalQuestions} questions ready
              </span>
            </div>
            <div className="generating-progress-bar">
              <div
                className="generating-progress-fill"
                style={{ width: totalQuestions > 0 ? `${(questions.length / totalQuestions) * 100}%` : '0%' }}
              />
            </div>
          </div>
        </div>
      )}

      <div className="exam-body">
        <div className="exam-main">
          {currentQ ? (
            <QuestionCard question={currentQ} index={currentQuestionIndex} />
          ) : (
            <div className="exam-generating-placeholder">
              <LoadingSpinner size={60} />
              <h3>Generating Question {currentQuestionIndex + 1}...</h3>
              <p>
                AI is currently crafting this question.<br/>
                You can explore other available questions using the palette while you wait!
              </p>
            </div>
          )}
        </div>
        <div className="exam-sidebar">
          <QuestionPalette />
        </div>
      </div>
      <div className="exam-nav">
        <Button variant="secondary" onClick={prevQuestion} disabled={currentQuestionIndex === 0}>Previous</Button>
        <Button variant="ghost" onClick={() => currentQ && clearAnswer(currentQ.id)} disabled={!currentQ}>Clear</Button>
        <Button variant="secondary" onClick={nextQuestion} disabled={currentQuestionIndex === (useExamStore.getState().currentTest?.total_questions || questions.length) - 1}>Next</Button>
      </div>
      <ExamSummaryModal isOpen={showSummary} onClose={() => setShowSummary(false)} onConfirm={handleSubmit} loading={submitting} />
    </div>
  );
}
