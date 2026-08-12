import React from 'react';
import { useNavigate } from 'react-router-dom';
import { MdPlayArrow, MdReplay, MdBookmark, MdBarChart } from 'react-icons/md';
import './Dashboard.css';

export default function QuickActions() {
  const navigate = useNavigate();
  const actions = [
    { icon: <MdPlayArrow />, title: 'New Test', desc: 'Start a fresh mock test', path: '/exams' },
    { icon: <MdReplay />, title: 'Continue', desc: 'Resume last test', path: '/exams' },
    { icon: <MdBookmark />, title: 'Bookmarks', desc: 'Review saved questions', path: '/profile' },
    { icon: <MdBarChart />, title: 'Analytics', desc: 'View performance', path: '/analytics' },
  ];
  return (
    <div className="quick-grid">
      {actions.map((a, i) => (
        <div className="quick-card" key={i} onClick={() => navigate(a.path)}>
          <div className="quick-card-icon">{a.icon}</div>
          <div className="quick-card-title">{a.title}</div>
          <div className="quick-card-desc">{a.desc}</div>
        </div>
      ))}
    </div>
  );
}
