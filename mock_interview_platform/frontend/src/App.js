import React, { useState } from 'react';
import './App.css';
import InterviewSetup from './pages/InterviewSetup';
import InterviewSession from './pages/InterviewSession';
import InterviewReport from './pages/InterviewReport';

function App() {
  const [currentPage, setCurrentPage] = useState('setup'); // setup, interview, report
  const [sessionData, setSessionData] = useState(null);

  const handleStartInterview = (data) => {
    setSessionData(data);
    setCurrentPage('interview');
  };

  const handleInterviewComplete = (reportData) => {
    setSessionData(reportData);
    setCurrentPage('report');
  };

  const handleStartNew = () => {
    setSessionData(null);
    setCurrentPage('setup');
  };

  return (
    <div className="App">
      {currentPage === 'setup' && <InterviewSetup onStart={handleStartInterview} />}
      {currentPage === 'interview' && (
        <InterviewSession
          sessionData={sessionData}
          onComplete={handleInterviewComplete}
        />
      )}
      {currentPage === 'report' && (
        <InterviewReport reportData={sessionData} onStartNew={handleStartNew} />
      )}
    </div>
  );
}

export default App;
