import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { examService } from '../services/examService';
import useExamStore from '../store/examStore';
import toast from 'react-hot-toast';
import './MockTestConfigPage.css';

const getApiBaseUrl = () => {
  const configuredUrl = import.meta.env.VITE_API_URL?.trim();
  if (configuredUrl) return configuredUrl.replace(/\/$/, '');
  return '/api';
};

export default function MockTestConfigPage() {
  const { examId } = useParams();
  const navigate = useNavigate();
  const { setTest } = useExamStore();
  const [exam, setExam] = useState(null);
  const [numQ, setNumQ] = useState(20);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [progress, setProgress] = useState({ completed: 0, total: 0, subject: '', percent: 0 });
  const abortRef = useRef(null);

  useEffect(() => {
    examService.getExam(examId).then(r => { setExam(r.data); setNumQ(Math.min(20, r.data.total_questions)); setLoading(false); }).catch(() => setLoading(false));
    return () => { if (abortRef.current) abortRef.current.abort(); };
  }, [examId]);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const response = await examService.generateMockTest(examId, numQ);
      const data = response.data;
      setTest(data, data.questions || []);
      toast.success('Mock test initializing! You can start right away.');
      navigate(`/exam/${data.id}`);
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to initialize test');
      setGenerating(false);
    }
  };

  if (loading) return <LoadingSpinner text="Loading exam..." />;
  if (!exam) return <div style={{ padding: 40, textAlign: 'center' }}>Exam not found</div>;

  return (
    <div className="config-page">
      <h1>Configure Mock Test</h1>
      <Card className="config-exam-info">
        <div className="config-exam-name">{exam.name}</div>
        <div className="exam-card-desc">{exam.description}</div>
        <div className="exam-card-stats">
          <span className="exam-stat"><strong>{exam.total_questions}</strong> Questions</span>
          <span className="exam-stat"><strong>{exam.duration_minutes}</strong> Minutes</span>
          <span className="exam-stat"><strong>{exam.total_marks}</strong> Marks</span>
        </div>
      </Card>
      <Card className="config-form">
        <div className="config-field">
          <label className="config-label">Number of Questions</label>
          <input type="range" className="config-slider" min={5} max={exam.total_questions} value={numQ} onChange={e => setNumQ(+e.target.value)} />
          <div className="config-value">{numQ} questions</div>
        </div>
      </Card>
      <Card className="config-instructions">
        <h3>📋 Instructions</h3>
        <ul>
          <li>Each question carries {exam.total_marks / exam.total_questions} mark(s).</li>
          <li>Negative marking: {exam.negative_marking} marks per wrong answer.</li>
          <li>Time limit: {exam.duration_minutes} minutes for full test (scaled for selected questions).</li>
          <li>You can mark questions for review and navigate freely.</li>
          <li>Test auto-submits when time runs out.</li>
        </ul>
      </Card>
      <Button variant="primary" size="lg" fullWidth onClick={handleGenerate} loading={generating}>🚀 Generate AI Mock Test</Button>
    </div>
  );
}
