import api from './api';
export const analyticsService = {
  getOverview: () => api.get('/analytics/overview'),
  getTopicPerformance: (examId) => api.get(`/analytics/topic-performance${examId ? `?exam_id=${examId}` : ''}`),
  getSubjectPerformance: () => api.get('/analytics/subject-performance'),
  getHistory: () => api.get('/analytics/history'),
  getWeakAreas: () => api.get('/analytics/weak-areas'),
};
