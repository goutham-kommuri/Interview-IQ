import React from 'react';
import '../styles/InterviewReport.css';

function InterviewReport({ reportData, onStartNew }) {
  const getReadinessColor = (readiness) => {
    switch (readiness?.toLowerCase()) {
      case 'highly ready':
        return '#4caf50';
      case 'ready':
        return '#8bc34a';
      case 'moderately ready':
        return '#ff9800';
      case 'needs improvement':
        return '#f44336';
      default:
        return '#2196f3';
    }
  };

  const formatScore = (score) => {
    return (score * 100).toFixed(1);
  };

  return (
    <div className="container report-container">
      <div className="report-header">
        <h1>📋 Interview Report</h1>
      </div>

      <div className="candidate-info">
        <h2>{reportData.candidate_name}</h2>
        <p className="job-title">{reportData.job_title}</p>
      </div>

      <div className="final-score-section">
        <div className="score-card">
          <span className="score-label">Final Score</span>
          <span className="final-score">{reportData.final_score.toFixed(2)}/100</span>
        </div>

        <div className="readiness-card">
          <span className="readiness-label">Readiness Level</span>
          <span
            className="readiness-value"
            style={{ color: getReadinessColor(reportData.readiness) }}
          >
            {reportData.readiness}
          </span>
        </div>

        <div className="hiring-card">
          <span className="hiring-label">Hiring Ready</span>
          <span className={`hiring-value ${reportData.hiring_ready ? 'yes' : 'no'}`}>
            {reportData.hiring_ready ? '✓ Yes' : '✗ No'}
          </span>
        </div>

        <div className="fit-card">
          <span className="fit-label">Role Fit</span>
          <span className="fit-value">{formatScore(reportData.role_fit)}%</span>
        </div>
      </div>

      <div className="duration-section">
        <p>
          Interview Duration: <strong>{reportData.duration_minutes.toFixed(1)} minutes</strong>
        </p>
      </div>

      <div className="report-section">
        <h3>Detailed Feedback</h3>
        <div className="report-content">
          {reportData.report.split('\n').map((line, idx) => (
            line.trim() && <p key={idx}>{line}</p>
          ))}
        </div>
      </div>

      <div className="action-buttons">
        <button onClick={onStartNew} className="btn btn-primary">
          Start New Interview
        </button>
        <button onClick={() => window.print()} className="btn btn-secondary">
          Print Report
        </button>
      </div>
    </div>
  );
}

export default InterviewReport;
