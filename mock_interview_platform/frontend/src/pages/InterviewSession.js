import React, { useState, useEffect } from 'react';
import { interviewAPI } from '../api/client';
import '../styles/InterviewSession.css';

function InterviewSession({ sessionData, onComplete }) {
  const [currentQuestion, setCurrentQuestion] = useState(sessionData.initialQuestion);
  const [answer, setAnswer] = useState('');
  const [timeStarted, setTimeStarted] = useState(Date.now());
  const [timeRemaining, setTimeRemaining] = useState(currentQuestion.time_limit);
  const [loading, setLoading] = useState(false);
  const [evaluation, setEvaluation] = useState(null);
  const [showEvaluation, setShowEvaluation] = useState(false);
  const [error, setError] = useState('');

  // Timer effect
  useEffect(() => {
    if (showEvaluation) return;

    const timer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - timeStarted) / 1000);
      const remaining = Math.max(0, currentQuestion.time_limit - elapsed);
      setTimeRemaining(remaining);

      if (remaining === 0) {
        handleSubmitAnswer();
      }
    }, 100);

    return () => clearInterval(timer);
  }, [timeStarted, showEvaluation, currentQuestion]);

  const handleSubmitAnswer = async () => {
    if (loading) return;

    const timeTaken = Math.floor((Date.now() - timeStarted) / 1000);

    if (!answer.trim()) {
      setError('Please provide an answer before submitting');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await interviewAPI.submitAnswer(
        sessionData.sessionId,
        answer,
        timeTaken
      );

      setEvaluation(result);
      setShowEvaluation(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to evaluate answer');
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = async () => {
    if (!evaluation.interview_continues) {
      // Interview concluded
      try {
        const report = await interviewAPI.concludeInterview(sessionData.sessionId);
        onComplete(report);
      } catch (err) {
        setError('Failed to get final report');
      }
    } else {
      // Move to next question
      setCurrentQuestion(evaluation.next_question);
      setAnswer('');
      setShowEvaluation(false);
      setTimeStarted(Date.now());
      setEvaluation(null);
    }
  };

  const progressPercentage =
    ((currentQuestion.question_number - 1) / currentQuestion.total_questions) * 100;

  return (
    <div className="container interview-container">
      <div className="interview-header">
        <div className="header-info">
          <h2>{sessionData.candidateName}</h2>
          <p>{sessionData.jobTitle}</p>
        </div>

        <div className="progress-section">
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${progressPercentage}%` }}
            ></div>
          </div>
          <p className="progress-text">
            Question {currentQuestion.question_number} of{' '}
            {currentQuestion.total_questions}
          </p>
        </div>
      </div>

      {!showEvaluation ? (
        <>
          <div className="question-section">
            <div className="question-meta">
              <span className={`difficulty difficulty-${currentQuestion.difficulty.toLowerCase()}`}>
                {currentQuestion.difficulty}
              </span>
              <span className="question-type">{currentQuestion.question_type}</span>
              <span className="time-limit">⏱️ {timeRemaining}s</span>
            </div>

            <div className="question-text">
              <p>{currentQuestion.question_text}</p>
            </div>

            {error && <div className="alert alert-error">{error}</div>}

            <div className="answer-input-section">
              <label htmlFor="answer">Your Answer:</label>
              <textarea
                id="answer"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Type your answer here..."
                disabled={loading}
              ></textarea>

              <button
                onClick={handleSubmitAnswer}
                className="btn btn-primary"
                disabled={loading || !answer.trim()}
              >
                {loading ? 'Evaluating...' : 'Submit Answer'}
              </button>
            </div>
          </div>
        </>
      ) : (
        <div className="evaluation-section">
          <div className="evaluation-header">
            <h3>📊 Answer Evaluation</h3>
            <div className="overall-score">
              <span className="score-label">Overall Score</span>
              <span className={`score-value score-${Math.round(evaluation.score / 20)}`}>
                {evaluation.score.toFixed(1)}/5.0
              </span>
            </div>
          </div>

          <div className="scoring-breakdown">
            <div className="score-item">
              <span className="score-name">Accuracy</span>
              <div className="score-bar">
                <div
                  className="score-bar-fill"
                  style={{ width: `${evaluation.accuracy * 20}%` }}
                ></div>
              </div>
              <span className="score-number">{evaluation.accuracy.toFixed(1)}/5</span>
            </div>

            <div className="score-item">
              <span className="score-name">Completeness</span>
              <div className="score-bar">
                <div
                  className="score-bar-fill"
                  style={{ width: `${evaluation.completeness * 20}%` }}
                ></div>
              </div>
              <span className="score-number">{evaluation.completeness.toFixed(1)}/5</span>
            </div>

            <div className="score-item">
              <span className="score-name">Clarity</span>
              <div className="score-bar">
                <div
                  className="score-bar-fill"
                  style={{ width: `${evaluation.clarity * 20}%` }}
                ></div>
              </div>
              <span className="score-number">{evaluation.clarity.toFixed(1)}/5</span>
            </div>

            <div className="score-item">
              <span className="score-name">Relevance</span>
              <div className="score-bar">
                <div
                  className="score-bar-fill"
                  style={{ width: `${evaluation.relevance * 20}%` }}
                ></div>
              </div>
              <span className="score-number">{evaluation.relevance.toFixed(1)}/5</span>
            </div>
          </div>

          <div className="feedback-section">
            <h4>Feedback</h4>
            <p>{evaluation.feedback}</p>
          </div>

          {evaluation.difficulty_adjusted && (
            <div className="alert alert-info">
              ✨ Difficulty adjusted to <strong>{evaluation.difficulty_new_level}</strong>
            </div>
          )}

          <button
            onClick={handleContinue}
            className="btn btn-primary"
            disabled={loading}
          >
            {evaluation.interview_continues ? 'Next Question' : 'View Final Report'}
          </button>
        </div>
      )}

      {loading && <div className="spinner"></div>}
    </div>
  );
}

export default InterviewSession;
