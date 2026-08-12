import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import { MdAutoAwesome, MdAllInclusive, MdPattern, MdAnalytics, MdTrendingUp, MdPhoneIphone } from 'react-icons/md';
import './HomePage.css';

const fadeUp = { initial: { opacity: 0, y: 30 }, whileInView: { opacity: 1, y: 0 }, viewport: { once: true }, transition: { duration: 0.6 } };

export default function HomePage() {
  const navigate = useNavigate();
  const features = [
    { icon: <MdAutoAwesome />, title: 'AI-Generated Questions', desc: 'Every test is unique with freshly generated questions powered by advanced AI.' },
    { icon: <MdAllInclusive />, title: 'Unlimited Mock Tests', desc: 'Practice as much as you want with no question repetition.' },
    { icon: <MdPattern />, title: 'Real Exam Patterns', desc: 'Questions follow actual exam patterns, syllabus, and difficulty levels.' },
    { icon: <MdAnalytics />, title: 'Detailed Analytics', desc: 'Track your performance with topic-wise and subject-wise analysis.' },
    { icon: <MdTrendingUp />, title: 'Track Progress', desc: 'Monitor your improvement over time with performance trends.' },
    { icon: <MdPhoneIphone />, title: 'Study Anywhere', desc: 'PWA app works on any device. Install and use offline.' },
  ];
  const categories = [
    { icon: '🚂', name: 'RRB' }, { icon: '📝', name: 'SSC' }, { icon: '🏦', name: 'Banking' }, { icon: '🏛️', name: 'UPSC' }, { icon: '🏢', name: 'State Gov' },
  ];
  return (
    <div className="home">
      <motion.section className="hero" {...fadeUp}>
        <div className="hero-content">
          <div className="hero-badge">🐝 AI-Powered Platform</div>
          <h1 className="hero-title">Ace Your <span className="gradient">Competitive Exams</span> With AI</h1>
          <p className="hero-subtitle">Generate unlimited, unique mock tests for RRB, SSC, Banking, UPSC & State exams. Never see the same question twice.</p>
          <div className="hero-buttons">
            <Button variant="primary" size="lg" onClick={() => navigate('/register')}>Get Started Free</Button>
            <Button variant="outline" size="lg" onClick={() => navigate('/login')}>Sign In</Button>
          </div>
        </div>
      </motion.section>
      <motion.section className="features" {...fadeUp}>
        <h2 className="section-title">Why MockBees?</h2>
        <p className="section-subtitle">Everything you need to crack your exam</p>
        <div className="features-grid">
          {features.map((f, i) => (
            <Card key={i} className="feature-card" hoverable>
              <div className="feature-icon">{f.icon}</div>
              <div className="feature-title">{f.title}</div>
              <div className="feature-desc">{f.desc}</div>
            </Card>
          ))}
        </div>
      </motion.section>
      <motion.section className="categories-section" {...fadeUp}>
        <h2 className="section-title">Exam Categories</h2>
        <p className="section-subtitle">Prepare for India's top competitive exams</p>
        <div className="features-grid">
          {categories.map((c, i) => (
            <Card key={i} className="category-card" hoverable onClick={() => navigate('/register')}>
              <div className="category-icon">{c.icon}</div>
              <div className="category-name">{c.name}</div>
            </Card>
          ))}
        </div>
      </motion.section>
      <motion.section className="stats-section" {...fadeUp}>
        <div className="stats-row">
          {[{ v: '10K+', l: 'Users' }, { v: '50K+', l: 'Tests Generated' }, { v: '500K+', l: 'Questions' }, { v: '98%', l: 'Satisfaction' }].map((s, i) => (
            <div className="home-stat" key={i}><div className="home-stat-value">{s.v}</div><div className="home-stat-label">{s.l}</div></div>
          ))}
        </div>
      </motion.section>
      <section className="cta-section">
        <h2 className="section-title">Ready to Start?</h2>
        <p className="section-subtitle">Join thousands of aspirants preparing smarter with AI</p>
        <Button variant="primary" size="lg" onClick={() => navigate('/register')}>Create Free Account</Button>
      </section>
    </div>
  );
}
