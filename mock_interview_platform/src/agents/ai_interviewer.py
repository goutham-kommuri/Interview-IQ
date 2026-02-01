"""AI Interviewer Agent for conducting mock interviews."""

import json
import time
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.utils import (
    CandidateProfile, JobRequirement, InterviewQuestion,
    AnswerEvaluation, InterviewScore, get_logger
)
from src.core import (
    ResumeAnalyzer, JobDescriptionAnalyzer, QuestionGenerator,
    AnswerEvaluator, InterviewScorer
)

logger = get_logger(__name__)


class AIInterviewer:
    """
    AI-powered interviewer agent that conducts mock interviews.
    
    Capabilities:
    - Analyze resume and job description
    - Generate adaptive interview questions
    - Evaluate answers in real-time
    - Adapt difficulty based on performance
    - Conduct early termination if needed
    - Generate comprehensive feedback
    """
    
    def __init__(self, config=None):
        """
        Initialize the AI Interviewer agent.
        
        Args:
            config: Configuration object with model and interview settings
        """
        self.logger = logger
        self.config = config
        
        # Initialize components
        self.resume_analyzer = ResumeAnalyzer()
        self.jd_analyzer = JobDescriptionAnalyzer()
        self.question_generator = QuestionGenerator()
        self.answer_evaluator = AnswerEvaluator()
        self.interview_scorer = InterviewScorer()
        
        # Interview state
        self.candidate_profile: Optional[CandidateProfile] = None
        self.job_requirement: Optional[JobRequirement] = None
        self.questions: List[InterviewQuestion] = []
        self.evaluations: List[AnswerEvaluation] = []
        self.current_question_index = 0
        self.early_termination_triggered = False
        self.interview_start_time = None
        self.interview_end_time = None
    
    def initialize_interview(self, resume_text: str, jd_text: str,
                           candidate_name: str = "Candidate",
                           job_title: str = "Tech Position") -> Dict[str, Any]:
        """
        Initialize an interview session.
        
        Args:
            resume_text: Candidate's resume in text format
            jd_text: Job description in text format
            candidate_name: Name of the candidate
            job_title: Title of the job position
            
        Returns:
            Dictionary with initialization status and interview info
        """
        self.logger.info(f"Initializing interview for {candidate_name}")
        self.interview_start_time = datetime.now()
        
        try:
            # Analyze resume and job description
            self.candidate_profile = self.resume_analyzer.analyze(
                resume_text, candidate_name
            )
            self.job_requirement = self.jd_analyzer.analyze(
                jd_text, job_title
            )
            
            # Identify skill gaps
            skill_gaps = self.jd_analyzer.identify_skill_gaps(
                self.candidate_profile, self.job_requirement
            )
            self.job_requirement.skill_gaps = skill_gaps
            
            # Generate questions
            num_questions = self.config.max_questions if self.config else 5
            self.questions = self.question_generator.generate_questions(
                self.candidate_profile, self.job_requirement, num_questions
            )
            
            self.logger.info(f"Interview initialized with {len(self.questions)} questions")
            
            return {
                "status": "success",
                "message": f"Interview ready for {candidate_name}",
                "candidate_name": candidate_name,
                "job_title": job_title,
                "total_questions": len(self.questions),
                "skill_gaps": skill_gaps[:3],
                "first_question": self.questions[0].question_text if self.questions else None,
            }
        except Exception as e:
            self.logger.error(f"Failed to initialize interview: {str(e)}")
            return {
                "status": "error",
                "message": f"Interview initialization failed: {str(e)}",
            }
    
    def get_current_question(self) -> Optional[Dict[str, Any]]:
        """Get the current interview question."""
        if self.current_question_index >= len(self.questions):
            return None
        
        question = self.questions[self.current_question_index]
        
        return {
            "question_number": self.current_question_index + 1,
            "total_questions": len(self.questions),
            "question_id": question.id,
            "question_text": question.question_text,
            "difficulty": question.difficulty.value,
            "skill_area": question.skill_area.value,
            "time_limit": question.time_limit,
            "question_type": question.question_type,
        }
    
    def evaluate_answer(self, answer_text: str, time_taken: int) -> Dict[str, Any]:
        """
        Evaluate candidate's answer to current question.
        
        Args:
            answer_text: Candidate's answer
            time_taken: Time taken to answer (seconds)
            
        Returns:
            Evaluation result with score and feedback
        """
        if self.current_question_index >= len(self.questions):
            return {"status": "error", "message": "No active question"}
        
        question = self.questions[self.current_question_index]
        
        # Evaluate the answer
        evaluation = self.answer_evaluator.evaluate(
            question, answer_text, time_taken
        )
        self.evaluations.append(evaluation)
        
        self.logger.info(f"Answer evaluated. Score: {evaluation.overall_score}")
        
        # Check for early termination
        if self._should_terminate_early():
            self.early_termination_triggered = True
            self.logger.warning("Interview terminated early due to poor performance")
        
        # Adapt difficulty for next question
        next_question_index = self.current_question_index + 1
        if next_question_index < len(self.questions):
            adapted_question = self.question_generator.adapt_difficulty(
                evaluation.overall_score,
                self.questions[next_question_index]
            )
            self.questions[next_question_index] = adapted_question
        
        # Move to next question
        self.current_question_index += 1
        
        result = {
            "status": "success",
            "overall_score": evaluation.overall_score,
            "accuracy": evaluation.accuracy_score,
            "clarity": evaluation.clarity_score,
            "depth": evaluation.depth_score,
            "relevance": evaluation.relevance_score,
            "time_efficiency": evaluation.time_efficiency_score,
            "feedback": evaluation.feedback,
            "strengths": evaluation.strengths,
            "areas_for_improvement": evaluation.areas_for_improvement,
            "key_points_covered": evaluation.key_points_covered,
            "missed_concepts": evaluation.missed_concepts,
        }
        
        # Add next question if available
        if not self.early_termination_triggered and self.current_question_index < len(self.questions):
            next_q = self.get_current_question()
            result["next_question"] = next_q
            result["interview_continues"] = True
        else:
            result["interview_continues"] = False
        
        return result
    
    def conclude_interview(self) -> InterviewScore:
        """
        Conclude the interview and generate final score.
        
        Returns:
            Final interview score with comprehensive feedback
        """
        self.interview_end_time = datetime.now()
        
        self.logger.info("Concluding interview and calculating final score")
        
        final_score = self.interview_scorer.calculate_score(
            self.evaluations,
            self.job_requirement,
            self.candidate_profile,
            self.questions,
            self.early_termination_triggered
        )
        
        return final_score
    
    def _should_terminate_early(self) -> bool:
        """Check if interview should be terminated early."""
        if len(self.evaluations) < 2:
            return False
        
        # Get last 3 evaluations
        recent_evals = self.evaluations[-3:]
        avg_recent_score = sum(e.overall_score for e in recent_evals) / len(recent_evals)
        
        threshold = self.config.early_termination_threshold if self.config else 40
        
        return avg_recent_score < threshold
    
    def get_interview_summary(self) -> Dict[str, Any]:
        """Get current interview summary."""
        if not self.evaluations:
            return {
                "questions_asked": self.current_question_index,
                "questions_answered": 0,
                "status": "In Progress",
            }
        
        avg_score = sum(e.overall_score for e in self.evaluations) / len(self.evaluations)
        
        return {
            "questions_asked": self.current_question_index,
            "questions_answered": len(self.evaluations),
            "current_average_score": round(avg_score, 2),
            "status": "Completed" if self.early_termination_triggered else "In Progress",
            "interview_duration": self._get_interview_duration(),
        }
    
    def _get_interview_duration(self) -> str:
        """Get interview duration in minutes:seconds format."""
        if not self.interview_start_time:
            return "0:00"
        
        end_time = self.interview_end_time or datetime.now()
        duration = int((end_time - self.interview_start_time).total_seconds())
        minutes = duration // 60
        seconds = duration % 60
        
        return f"{minutes}:{seconds:02d}"
    
    def generate_interview_report(self) -> str:
        """Generate detailed interview report."""
        if not self.evaluations:
            return "No interview data available"
        
        final_score = self.conclude_interview()
        
        report = []
        report.append("=" * 80)
        report.append("MOCK INTERVIEW REPORT")
        report.append("=" * 80)
        report.append(f"\nCandidate: {self.candidate_profile.name}")
        report.append(f"Position: {self.job_requirement.title}")
        report.append(f"Interview Date: {self.interview_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Duration: {self._get_interview_duration()}")
        
        report.append("\n" + "=" * 80)
        report.append("OVERALL PERFORMANCE")
        report.append("=" * 80)
        report.append(f"Final Score: {final_score.total_score}/100")
        report.append(f"Readiness Category: {final_score.readiness_category}")
        report.append(f"Hiring Readiness: {final_score.hiring_readiness_indicator}")
        report.append(f"Estimated Role Fit: {final_score.estimated_role_fit}%")
        report.append(f"Completion: {final_score.interview_completion_percentage}%")
        
        report.append("\n" + "=" * 80)
        report.append("SKILL AREA BREAKDOWN")
        report.append("=" * 80)
        for skill_area, score in final_score.skill_area_scores.items():
            report.append(f"  {skill_area}: {score.score}/100 ({score.questions_asked} questions)")
        
        report.append("\n" + "=" * 80)
        report.append("COMPONENT SCORES")
        report.append("=" * 80)
        report.append(f"Technical Depth: {final_score.technical_depth}/100")
        report.append(f"Communication Quality: {final_score.communication_quality}/100")
        report.append(f"Time Management: {final_score.time_management_score}/100")
        report.append(f"Adaptability: {final_score.adaptability_score}/100")
        
        report.append("\n" + "=" * 80)
        report.append("STRENGTHS")
        report.append("=" * 80)
        for strength in final_score.strengths:
            report.append(f"  ✓ {strength}")
        
        report.append("\n" + "=" * 80)
        report.append("AREAS FOR IMPROVEMENT")
        report.append("=" * 80)
        for weakness in final_score.weaknesses:
            report.append(f"  ✗ {weakness}")
        
        report.append("\n" + "=" * 80)
        report.append("ACTIONABLE FEEDBACK")
        report.append("=" * 80)
        for feedback in final_score.actionable_feedback:
            report.append(f"  • {feedback}")
        
        report.append("\n" + "=" * 80)
        report.append("INDIVIDUAL QUESTION SCORES")
        report.append("=" * 80)
        for i, eval in enumerate(self.evaluations, 1):
            report.append(f"\nQuestion {i}: {eval.overall_score}/100")
            report.append(f"  Accuracy: {eval.accuracy_score} | Clarity: {eval.clarity_score} | "
                         f"Depth: {eval.depth_score} | Relevance: {eval.relevance_score}")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
