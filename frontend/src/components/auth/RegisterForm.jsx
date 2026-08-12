import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { MdEmail, MdLock, MdPerson } from 'react-icons/md';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useAuthStore } from '../../store/authStore';
import Input from '../common/Input';
import Button from '../common/Button';
import './AuthForms.css';

const RegisterForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const { register, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      toast.error("Passwords don't match");
      return;
    }
    try {
      await register(name, email, password);
      toast.success('Account created successfully!');
      navigate('/dashboard');
    } catch (error) {
      const message = error.response?.data?.detail || error.response?.data?.message || 'Registration failed';
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
        <h2>Create Account</h2>
        <p>Start your journey to success</p>
      </div>

      <form onSubmit={handleSubmit} className="auth-form">
        <Input
          label="Full Name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          icon={<MdPerson />}
          required
          placeholder="Enter your full name"
        />

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
          placeholder="Create a password"
        />

        <Input
          label="Confirm Password"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          icon={<MdLock />}
          required
          placeholder="Confirm your password"
        />

        <Button type="submit" variant="primary" fullWidth loading={isLoading}>
          Sign Up
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
        Sign up with Google
      </Button>

      <div className="auth-footer">
        Already have an account? <Link to="/login">Login</Link>
      </div>
    </motion.div>
  );
};

export default RegisterForm;
