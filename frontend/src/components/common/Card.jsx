import React from 'react';

export default function Card({ children, className = '', onClick, hoverable = false, style }) {
  return (
    <div
      className={`glass-card ${hoverable ? 'glass-card-hoverable' : ''} ${className}`}
      onClick={onClick}
      style={{ cursor: onClick ? 'pointer' : 'default', ...style }}
    >
      {children}
    </div>
  );
}
