import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import ResultSummary from '../components/results/ResultSummary';
import QuestionReview from '../components/results/QuestionReview';
import ScoreBreakdown from '../components/analytics/ScoreBreakdown';
import AIRecommendations from '../components/results/AIRecommendations';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { examService } from '../services/examService';
import './ResultsPage.css';

export default function ResultsPage() {
  const { testId } = useParams();
  const [result, setResult] = useState(null);
  const [tab, setTab] = useState('review');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    examService.getTestAttempt(testId).then(r => { setResult(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, [testId]);

  if (loading) return <LoadingSpinner text="Loading results..." />;
  if (!result) return <div style={{ padding: 40, textAlign: 'center' }}>Results not found</div>;

  const answers = {};
  (result.user_answers || []).forEach(a => { answers[a.question_id] = a.selected_answer; });

  return (
    <div className="results-page">
      <h1>Test Results 📊</h1>
      <ResultSummary result={result} />
      <div className="review-tabs">
        <button className={`review-tab ${tab === 'review' ? 'active' : ''}`} onClick={() => setTab('review')}>Review</button>
        <button className={`review-tab ${tab === 'analytics' ? 'active' : ''}`} onClick={() => setTab('analytics')}>Analytics</button>
        <button className={`review-tab ${tab === 'tips' ? 'active' : ''}`} onClick={() => setTab('tips')}>Tips</button>
      </div>
      {tab === 'review' && <QuestionReview questions={result.questions || []} answers={answers} />}
      {tab === 'analytics' && <ScoreBreakdown correct={result.correct_answers} incorrect={result.incorrect_answers} unanswered={result.unanswered} />}
      {tab === 'tips' && <AIRecommendations weakAreas={[]} score={result.accuracy} />}
    </div>
  );
}
