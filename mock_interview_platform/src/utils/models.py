"""Data models for the mock interview platform."""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


class QuestionDifficulty(str, Enum):
    """Difficulty levels for interview questions."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class SkillArea(str, Enum):
    """Skill areas for evaluation."""
    TECHNICAL = "technical"
    PROBLEM_SOLVING = "problem_solving"
    COMMUNICATION = "communication"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"


@dataclass
class CandidateProfile:
    """Candidate profile extracted from resume."""
    name: str
    email: str
    phone: str
    years_of_experience: int
    skills: List[str]
    technologies: List[str]
    projects: List[Dict[str, str]]
    education: List[Dict[str, str]]
    certifications: List[str]
    summary: str = ""
    strengths: List[str] = field(default_factory=list)


@dataclass
class JobRequirement:
    """Job requirements extracted from JD."""
    title: str
    required_skills: List[str]
    preferred_skills: List[str]
    technologies: List[str]
    experience_level: str
    key_responsibilities: List[str]
    nice_to_have: List[str]
    role_description: str = ""
    skill_gaps: List[str] = field(default_factory=list)


@dataclass
class InterviewQuestion:
    """Interview question data structure."""
    id: str
    question_text: str
    difficulty: QuestionDifficulty
    skill_area: SkillArea
    question_type: str  # technical, behavioral, scenario-based, conceptual
    expected_concepts: List[str]
    ideal_answer_points: List[str]
    time_limit: int = 120  # seconds


@dataclass
class AnswerEvaluation:
    """Evaluation of a candidate's answer."""
    question_id: str
    answer_text: str
    time_taken: int  # seconds
    accuracy_score: float  # 0-100
    clarity_score: float  # 0-100
    depth_score: float  # 0-100
    relevance_score: float  # 0-100
    time_efficiency_score: float  # 0-100
    overall_score: float  # 0-100
    feedback: str
    strengths: List[str]
    areas_for_improvement: List[str]
    key_points_covered: List[str]
    missed_concepts: List[str]


@dataclass
class SkillAreaScore:
    """Score for a specific skill area."""
    skill_area: SkillArea
    score: float  # 0-100
    questions_asked: int
    average_performance: float


@dataclass
class InterviewScore:
    """Overall interview score and feedback."""
    total_score: float  # 0-100
    skill_area_scores: Dict[str, SkillAreaScore]
    question_scores: List[float]
    strengths: List[str]
    weaknesses: List[str]
    readiness_category: str  # "Strong", "Average", "Needs Improvement"
    hiring_readiness_indicator: str  # "Ready", "Needs Development", "Not Ready"
    actionable_feedback: List[str]
    estimated_role_fit: float  # 0-100
    time_management_score: float  # 0-100
    adaptability_score: float  # 0-100
    technical_depth: float  # 0-100
    communication_quality: float  # 0-100
    interview_completion_percentage: float  # 0-100
