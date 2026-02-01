import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const interviewAPI = {
  // Initialize a new interview session
  initializeInterview: async (candidateName, jobTitle, resumeText, jdText) => {
    const response = await apiClient.post('/api/interview/initialize', {
      candidate_name: candidateName,
      job_title: jobTitle,
      resume_text: resumeText,
      jd_text: jdText,
    });
    return response.data;
  },

  // Get current question
  getCurrentQuestion: async (sessionId) => {
    const response = await apiClient.get(`/api/interview/${sessionId}/question`);
    return response.data;
  },

  // Submit answer for evaluation
  submitAnswer: async (sessionId, answerText, timeTaken) => {
    const response = await apiClient.post(
      `/api/interview/${sessionId}/submit-answer`,
      {
        session_id: sessionId,
        answer_text: answerText,
        time_taken: timeTaken,
      }
    );
    return response.data;
  },

  // Conclude interview and get report
  concludeInterview: async (sessionId) => {
    const response = await apiClient.get(`/api/interview/${sessionId}/conclude`);
    return response.data;
  },

  // Delete a session
  deleteSession: async (sessionId) => {
    const response = await apiClient.delete(`/api/interview/${sessionId}`);
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/api/health');
    return response.data;
  },
};

export default apiClient;
