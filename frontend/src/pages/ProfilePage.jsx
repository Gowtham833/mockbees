import React, { useState } from 'react';
import Card from '../components/common/Card';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import useAuthStore from '../store/authStore';
import toast from 'react-hot-toast';
import './ProfilePage.css';

export default function ProfilePage() {
  const { user } = useAuthStore();
  const [name, setName] = useState(user?.name || '');

  const handleSave = () => { toast.success('Profile updated!'); };

  return (
    <div className="profile-page">
      <h1>Profile 👤</h1>
      <Card className="profile-card">
        <div className="profile-avatar">{user?.name?.[0]?.toUpperCase() || '?'}</div>
        <div className="profile-name">{user?.name || 'Student'}</div>
        <div className="profile-email">{user?.email}</div>
        <div className="profile-joined">Member since {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'recently'}</div>
      </Card>
      <Card className="profile-form">
        <Input label="Name" value={name} onChange={e => setName(e.target.value)} />
        <Input label="Email" value={user?.email || ''} disabled />
        <Button variant="primary" onClick={handleSave}>Save Changes</Button>
      </Card>
    </div>
  );
}
