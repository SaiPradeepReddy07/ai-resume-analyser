import api from './api';

export async function fetchDashboardStats() {
  const response = await api.get('/dashboard/stats');
  return response.data;
}

export async function fetchHistory() {
  const response = await api.get('/analysis');
  return response.data;
}

export async function fetchAnalysis(id) {
  const response = await api.get(`/analysis/${id}`);
  return response.data;
}

export async function submitAnalysis(formData) {
  const response = await api.post('/analysis/direct', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
}
