import React from 'react';
import './LoadingSpinner.css';

export default function LoadingSpinner({ size = 40, text }) {
  return (
    <div className="spinner-container">
      <div className="spinner" style={{ width: size, height: size }}>
        <div className="spinner-ring" />
        <span className="spinner-bee">🐝</span>
      </div>
      {text && <p className="spinner-text">{text}</p>}
    </div>
  );
}
