import React from 'react';
import { motion } from 'framer-motion';
import LoginForm from '../components/auth/LoginForm';
import './AuthPages.css';

export default function LoginPage() {
  return (
    <div className="auth-page">
      <motion.div className="auth-container" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
        <div className="auth-brand">
          <div className="auth-brand-logo">🐝</div>
          <div className="auth-brand-name">MockBees</div>
          <div className="auth-brand-tagline">AI-Powered Exam Preparation</div>
        </div>
        <LoginForm />
      </motion.div>
    </div>
  );
}
