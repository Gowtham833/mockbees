import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { examService } from '../services/examService';
import './ExamSelectionPage.css';

export default function ExamSelectionPage() {
  const [categories, setCategories] = useState([]);
  const [selected, setSelected] = useState(null);
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    examService.getCategories().then(r => { setCategories(r.data || []); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const selectCategory = async (cat) => {
    setSelected(cat.id);
    try {
      const r = await examService.getCategoryExams(cat.id);
      setExams(r.data?.exams || r.data || []);
    } catch (e) { console.error(e); }
  };

  if (loading) return <LoadingSpinner text="Loading exams..." />;

  return (
    <div className="exam-selection">
      <h1>Choose Your Exam 📋</h1>
      <div className="category-filters">
        <button className={`filter-btn ${!selected ? 'active' : ''}`} onClick={() => { setSelected(null); setExams([]); }}>All</button>
        {categories.map(c => (
          <button key={c.id} className={`filter-btn ${selected === c.id ? 'active' : ''}`} onClick={() => selectCategory(c)}>
            {c.icon} {c.name}
          </button>
        ))}
      </div>
      {!selected ? (
        <div className="exams-grid">
          {categories.map(c => (
            <Card key={c.id} className="exam-card" hoverable onClick={() => selectCategory(c)}>
              <div style={{ fontSize: '2.5rem', marginBottom: 12 }}>{c.icon}</div>
              <div className="exam-card-name">{c.name}</div>
              <div className="exam-card-desc">{c.description}</div>
            </Card>
          ))}
        </div>
      ) : (
        <div className="exams-grid">
          {exams.map(e => (
            <Card key={e.id} className="exam-card">
              <div className="exam-card-name">{e.name}</div>
              <div className="exam-card-desc">{e.description}</div>
              <div className="exam-card-stats">
                <span className="exam-stat"><strong>{e.total_questions}</strong> Questions</span>
                <span className="exam-stat"><strong>{e.duration_minutes}</strong> Minutes</span>
                <span className="exam-stat"><strong>{e.total_marks}</strong> Marks</span>
                <span className="exam-stat">-<strong>{e.negative_marking}</strong> Negative</span>
              </div>
              <Button variant="primary" fullWidth onClick={() => navigate(`/exams/${e.id}/config`)}>Start Test</Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
