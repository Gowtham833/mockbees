import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Button from '../components/common/Button';

export default function NotFoundPage() {
  const navigate = useNavigate();
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 40, textAlign: 'center' }}>
      <motion.div animate={{ y: [0, -15, 0] }} transition={{ duration: 2, repeat: Infinity }} style={{ fontSize: '4rem', marginBottom: 20 }}>🐝</motion.div>
      <h1 style={{ fontSize: '4rem', fontWeight: 800, background: 'linear-gradient(135deg, #f59e0b, #ef4444)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', marginBottom: 12 }}>404</h1>
      <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', marginBottom: 32 }}>Oops! This page doesn't exist.</p>
      <Button variant="primary" onClick={() => navigate('/')}>Go Home</Button>
    </div>
  );
}
