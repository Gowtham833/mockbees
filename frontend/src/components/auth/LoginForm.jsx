import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { MdEmail, MdLock } from 'react-icons/md';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useAuthStore } from '../../store/authStore';
import Input from '../common/Input';
import Button from '../common/Button';
import './AuthForms.css';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      toast.success('Welcome back!');
      navigate('/dashboard');
    } catch (error) {
      const message = error.response?.data?.detail || error.response?.data?.message || 'Login failed';
      toast.error(message);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="auth-card glass-card"
    >
      <div className="auth-header">
        <h2>Welcome Back</h2>
        <p>Login to continue your preparation</p>
      </div>

      <form onSubmit={handleSubmit} className="auth-form">
        <Input
          label="Email Address"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          icon={<MdEmail />}
          required
          placeholder="Enter your email"
        />
        
        <Input
          label="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          icon={<MdLock />}
          required
          placeholder="Enter your password"
        />

        <div className="auth-options">
          <label className="checkbox-container">
            <input type="checkbox" />
            <span className="checkmark"></span>
            Remember me
          </label>
          <a href="#" className="forgot-password">Forgot Password?</a>
        </div>

        <Button type="submit" variant="primary" fullWidth loading={isLoading}>
          Sign In
        </Button>
      </form>

      <div className="auth-divider">
        <span>OR</span>
      </div>

      <Button 
        variant="outline" 
        fullWidth 
        onClick={() => toast('Coming soon!', { icon: '🚧' })}
      >
        <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/google/google-original.svg" alt="Google" className="google-icon" />
        Continue with Google
      </Button>

      <div className="auth-footer">
        Don't have an account? <Link to="/register">Sign up</Link>
      </div>
    </motion.div>
  );
};

export default LoginForm;
