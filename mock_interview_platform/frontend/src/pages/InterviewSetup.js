import React, { useState } from 'react';
import { interviewAPI } from '../api/client';
import '../styles/InterviewSetup.css';

function InterviewSetup({ onStart }) {
  const [formData, setFormData] = useState({
    candidateName: '',
    jobTitle: '',
    resume: '',
    jobDescription: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.candidateName.trim()) {
      setError('Candidate name is required');
      return;
    }

    if (!formData.jobTitle.trim()) {
      setError('Job title is required');
      return;
    }

    if (!formData.resume.trim()) {
      setError('Resume is required');
      return;
    }

    if (!formData.jobDescription.trim()) {
      setError('Job description is required');
      return;
    }

    setLoading(true);

    try {
      const response = await interviewAPI.initializeInterview(
        formData.candidateName,
        formData.jobTitle,
        formData.resume,
        formData.jobDescription
      );

      onStart({
        sessionId: response.session_id,
        candidateName: formData.candidateName,
        jobTitle: formData.jobTitle,
        initialQuestion: response.initial_question,
        skillGaps: response.skill_gaps,
        totalQuestions: response.total_questions,
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to initialize interview. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container setup-container">
      <div className="header">
        <h1>🎯 Mock Interview Platform</h1>
        <p>Prepare for your next interview with AI-powered mock interviews</p>
      </div>

      <form onSubmit={handleSubmit}>
        {error && <div className="alert alert-error">{error}</div>}

        <div className="form-group">
          <label htmlFor="candidateName">Your Name</label>
          <input
            type="text"
            id="candidateName"
            name="candidateName"
            value={formData.candidateName}
            onChange={handleChange}
            placeholder="e.g., John Doe"
          />
        </div>

        <div className="form-group">
          <label htmlFor="jobTitle">Job Title</label>
          <input
            type="text"
            id="jobTitle"
            name="jobTitle"
            value={formData.jobTitle}
            onChange={handleChange}
            placeholder="e.g., Senior Software Engineer"
          />
        </div>

        <div className="form-group">
          <label htmlFor="resume">Your Resume</label>
          <textarea
            id="resume"
            name="resume"
            value={formData.resume}
            onChange={handleChange}
            placeholder="Paste your resume here..."
          />
        </div>

        <div className="form-group">
          <label htmlFor="jobDescription">Job Description</label>
          <textarea
            id="jobDescription"
            name="jobDescription"
            value={formData.jobDescription}
            onChange={handleChange}
            placeholder="Paste the job description here..."
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Initializing Interview...' : 'Start Interview'}
        </button>
      </form>

      {loading && <div className="spinner"></div>}
    </div>
  );
}

export default InterviewSetup;
