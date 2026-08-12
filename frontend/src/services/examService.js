import api from './api';
export const examService = {
  getCategories: () => api.get('/exams/categories'),
  getCategoryExams: (categoryId) => api.get(`/exams/categories/${categoryId}`),
  getExam: (examId) => api.get(`/exams/${examId}`),
  generateMockTest: (examId, numQuestions) => api.post('/mock-tests/generate', { exam_id: examId, num_questions: numQuestions }),
  getTestAttempt: (attemptId) => api.get(`/mock-tests/${attemptId}`),
  saveAnswer: (attemptId, data) => api.post(`/mock-tests/${attemptId}/save-answer`, data),
  submitTest: (attemptId, data) => api.post(`/mock-tests/${attemptId}/submit`, data),
  getHistory: () => api.get('/mock-tests/history'),
};
