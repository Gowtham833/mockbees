import api from './api';
export const authService = {
  login: (email, password) => {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    return api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
  },
  register: (name, email, password) => api.post('/auth/register', { name, email, password }),
  getProfile: () => api.get('/auth/me'),
  refreshToken: (refreshToken) => api.post(`/auth/refresh?refresh_token=${refreshToken}`),
};

