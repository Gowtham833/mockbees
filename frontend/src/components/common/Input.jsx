import React from 'react';
import './Input.css';

export default function Input({ label, type = 'text', value, onChange, placeholder, error, icon, required, name, ...props }) {
  return (
    <div className={`input-group ${error ? 'input-error' : ''}`}>
      {label && <label className="input-label">{label}{required && <span className="required">*</span>}</label>}
      <div className="input-wrapper">
        {icon && <span className="input-icon">{icon}</span>}
        <input
          className="input-field"
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          name={name}
          required={required}
          {...props}
        />
      </div>
      {error && <span className="input-error-msg">{error}</span>}
    </div>
  );
}
