"""FastAPI application for the mock interview platform."""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

from src.main import InterviewOrchestrator
from src.utils import Config, get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="InterviewIQ API",
    description="InterviewIQ - AI-powered mock interview platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for interview sessions
interview_sessions: Dict[str, InterviewOrchestrator] = {}

# Request/Response Models
class InterviewInitRequest(BaseModel):
    """Request model for initializing an interview."""
    candidate_name: str
    job_title: str
    resume_text: str
    jd_text: str

class InterviewInitResponse(BaseModel):
    """Response model for interview initialization."""
    session_id: str
    status: str
    message: str
    skill_gaps: List[str]
    total_questions: int
    initial_question: Dict[str, Any]

class QuestionResponse(BaseModel):
    """Response model for a question."""
    question_number: int
    total_questions: int
    difficulty: str
    time_limit: int
    question_type: str
    question_text: str
    session_id: str

class AnswerSubmitRequest(BaseModel):
    """Request model for submitting an answer."""
    session_id: str
    answer_text: str
    time_taken: int

class AnswerEvaluationResponse(BaseModel):
    """Response model for answer evaluation."""
    session_id: str
    score: float
    accuracy: float
    completeness: float
    clarity: float
    relevance: float
    feedback: str
    interview_continues: bool
    next_question: Optional[Dict[str, Any]] = None
    difficulty_adjusted: bool
    difficulty_new_level: Optional[str] = None

class InterviewReportResponse(BaseModel):
    """Response model for final interview report."""
    session_id: str
    status: str
    candidate_name: str
    job_title: str
    final_score: float
    readiness: str
    hiring_ready: bool
    role_fit: float
    report: str
    duration_minutes: float

# API Endpoints
@app.post("/api/interview/initialize", response_model=InterviewInitResponse)
async def initialize_interview(request: InterviewInitRequest) -> InterviewInitResponse:
    """Initialize a new interview session."""
    try:
        logger.info(f"Initializing interview for {request.candidate_name}")
        
        # Create orchestrator
        config = Config()
        orchestrator = InterviewOrchestrator(config)
        
        # Initialize interview
        init_result = orchestrator.run_interview(
            resume_text=request.resume_text,
            jd_text=request.jd_text,
            candidate_name=request.candidate_name,
            job_title=request.job_title,
            interactive=False  # Non-interactive for API
        )
        
        # Generate session ID
        session_id = f"session_{datetime.now().timestamp()}"
        interview_sessions[session_id] = orchestrator
        
        # Get first question
        first_question = orchestrator.interviewer.get_current_question()
        
        return InterviewInitResponse(
            session_id=session_id,
            status=init_result.get("status", "success"),
            message=init_result.get("message", "Interview initialized"),
            skill_gaps=init_result.get("skill_gaps", []),
            total_questions=init_result.get("total_questions", 5),
            initial_question=first_question
        )
    except Exception as e:
        logger.error(f"Error initializing interview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/interview/{session_id}/question", response_model=QuestionResponse)
async def get_current_question(session_id: str) -> QuestionResponse:
    """Get the current question for an interview session."""
    try:
        if session_id not in interview_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        orchestrator = interview_sessions[session_id]
        question = orchestrator.interviewer.get_current_question()
        
        if not question:
            raise HTTPException(status_code=400, detail="No more questions in this interview")
        
        return QuestionResponse(
            session_id=session_id,
            **question
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interview/{session_id}/submit-answer", response_model=AnswerEvaluationResponse)
async def submit_answer(session_id: str, request: AnswerSubmitRequest) -> AnswerEvaluationResponse:
    """Submit an answer for evaluation."""
    try:
        if session_id not in interview_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        orchestrator = interview_sessions[session_id]
        
        # Evaluate answer
        evaluation = orchestrator.interviewer.evaluate_answer(
            request.answer_text,
            request.time_taken
        )
        
        # Get next question if interview continues
        next_question = None
        if evaluation.get("interview_continues", False):
            next_question = orchestrator.interviewer.get_current_question()
        
        return AnswerEvaluationResponse(
            session_id=session_id,
            score=evaluation.get("overall_score", 0),
            accuracy=evaluation.get("accuracy_score", 0),
            completeness=evaluation.get("completeness_score", 0),
            clarity=evaluation.get("clarity_score", 0),
            relevance=evaluation.get("relevance_score", 0),
            feedback=evaluation.get("feedback", ""),
            interview_continues=evaluation.get("interview_continues", False),
            next_question=next_question,
            difficulty_adjusted=evaluation.get("difficulty_adjusted", False),
            difficulty_new_level=evaluation.get("new_difficulty", None)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/interview/{session_id}/conclude", response_model=InterviewReportResponse)
async def conclude_interview(session_id: str) -> InterviewReportResponse:
    """Conclude an interview and get the final report."""
    try:
        if session_id not in interview_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        orchestrator = interview_sessions[session_id]
        
        # Generate report and conclude
        report = orchestrator.interviewer.generate_interview_report()
        final_score = orchestrator.interviewer.conclude_interview()
        
        # Calculate duration
        start_time = orchestrator.interviewer.interview_start_time
        end_time = orchestrator.interviewer.interview_end_time or datetime.now()
        duration_minutes = (end_time - start_time).total_seconds() / 60
        
        return InterviewReportResponse(
            session_id=session_id,
            status="completed",
            candidate_name=orchestrator.interviewer.candidate_profile.name,
            job_title=orchestrator.interviewer.job_requirement.title,
            final_score=final_score.total_score,
            readiness=final_score.readiness_category,
            hiring_ready=final_score.hiring_readiness_indicator,
            role_fit=final_score.estimated_role_fit,
            report=report,
            duration_minutes=duration_minutes
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error concluding interview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/interview/{session_id}")
async def delete_session(session_id: str):
    """Delete an interview session."""
    try:
        if session_id not in interview_sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        del interview_sessions[session_id]
        return {"status": "success", "message": "Session deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
