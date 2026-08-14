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
    setProgress({ completed: 0, total: 0, subject: 'Initializing...', percent: 0 });

    const token = localStorage.getItem('mockbees_token');
    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const response = await fetch(`${getApiBaseUrl()}/mock-tests/generate-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ exam_id: parseInt(examId), num_questions: numQ }),
        signal: controller.signal
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          try {
            const event = JSON.parse(line.slice(6));

            if (event.type === 'progress') {
              const pct = event.total > 0 ? Math.round((event.completed / event.total) * 100) : 0;
              setProgress({
                completed: event.completed,
                total: event.total,
                subject: event.subject,
                percent: pct
              });
            } else if (event.type === 'complete') {
              const data = event.data;
              setTest(data, data.questions || []);
              toast.success('Mock test generated!');
              navigate(`/exam/${data.id}`);
              return;
            } else if (event.type === 'error') {
              throw new Error(event.message);
            }
          } catch (parseErr) {
            if (parseErr.message && !parseErr.message.includes('JSON')) throw parseErr;
          }
        }
      }

      // If we reach here without complete event, fallback
      throw new Error('Stream ended without completion');

    } catch (e) {
      if (e.name === 'AbortError') return;
      console.warn('SSE failed, falling back to regular endpoint:', e.message);
      
      // Fallback to regular non-streaming endpoint
      try {
        setProgress({ completed: 0, total: 0, subject: 'Generating questions...', percent: 0 });
        const r = await examService.generateMockTest(examId, numQ);
        const data = r.data;
        setTest(data, data.questions || []);
        toast.success('Mock test generated!');
        navigate(`/exam/${data.id}`);
        return;
      } catch (fallbackErr) {
        toast.error(fallbackErr.response?.data?.detail || 'Failed to generate test');
      }
      setGenerating(false);
    }
  };

  if (loading) return <LoadingSpinner text="Loading exam..." />;
  if (!exam) return <div style={{ padding: 40, textAlign: 'center' }}>Exam not found</div>;

  return (
    <div className="config-page">
      {generating && (
        <div className="generating-overlay">
          <div className="gen-progress-container">
            <div className="gen-bee-icon">
              <LoadingSpinner size={56} />
            </div>
            <div className="gen-progress-title">🐝 AI is generating your test...</div>
            <div className="gen-progress-subtitle">
              {progress.subject
                ? `Working on: ${progress.subject}`
                : 'Initializing AI engine...'
              }
            </div>
            <div className="gen-progress-bar-container">
              <div className="gen-progress-bar-track">
                <div
                  className="gen-progress-bar-fill"
                  style={{ width: `${Math.max(progress.percent, 5)}%` }}
                />
                <div className="gen-progress-bar-glow" style={{ width: `${Math.max(progress.percent, 5)}%` }} />
              </div>
              <div className="gen-progress-stats">
                {progress.total > 0 ? (
                  <>
                    <span className="gen-progress-count">{progress.completed} / {progress.total} batches</span>
                    <span className="gen-progress-pct">{progress.percent}%</span>
                  </>
                ) : (
                  <span className="gen-progress-count">Preparing batches...</span>
                )}
              </div>
            </div>
            <div className="gen-progress-tip">
              💡 Questions are generated in small parallel batches for speed
            </div>
          </div>
        </div>
      )}
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
