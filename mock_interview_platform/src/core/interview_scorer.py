"""Interview scorer for calculating final scores and feedback."""

from typing import List, Dict
from src.utils import (
    AnswerEvaluation, InterviewScore, SkillAreaScore, SkillArea,
    JobRequirement, CandidateProfile, get_logger
)

logger = get_logger(__name__)


class InterviewScorer:
    """Calculate and generate comprehensive interview scores."""
    
    # Skill area weights for overall score
    SKILL_WEIGHTS = {
        SkillArea.TECHNICAL: 0.30,
        SkillArea.PROBLEM_SOLVING: 0.25,
        SkillArea.BEHAVIORAL: 0.15,
        SkillArea.COMMUNICATION: 0.15,
        SkillArea.SYSTEM_DESIGN: 0.15,
    }
    
    def __init__(self):
        """Initialize the interview scorer."""
        self.logger = logger
    
    def calculate_score(self, evaluations: List[AnswerEvaluation],
                       job_requirement: JobRequirement,
                       candidate: CandidateProfile,
                       questions: List,
                       early_termination: bool = False) -> InterviewScore:
        """
        Calculate comprehensive interview score.
        
        Args:
            evaluations: List of answer evaluations
            job_requirement: Job requirements
            candidate: Candidate profile
            questions: List of interview questions
            early_termination: Whether interview was terminated early
            
        Returns:
            Comprehensive interview score
        """
        self.logger.info("Calculating interview score")
        
        if not evaluations:
            return self._create_zero_score()
        
        # Group evaluations by skill area
        skill_evaluations = self._group_by_skill_area(evaluations, questions)
        
        # Calculate scores by skill area
        skill_area_scores = {}
        for skill_area, eval_list in skill_evaluations.items():
            skill_area_scores[skill_area.value] = self._calculate_skill_area_score(
                skill_area, eval_list
            )
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(skill_area_scores)
        
        # Calculate component scores
        time_management_score = self._calculate_time_management_score(evaluations, questions)
        adaptability_score = self._calculate_adaptability_score(evaluations)
        technical_depth = skill_area_scores.get(SkillArea.TECHNICAL.value, 
                                               SkillAreaScore(SkillArea.TECHNICAL, 0, 0, 0)).score
        communication_quality = skill_area_scores.get(SkillArea.COMMUNICATION.value,
                                                     SkillAreaScore(SkillArea.COMMUNICATION, 0, 0, 0)).score
        
        # Calculate completion percentage
        completion_percentage = self._calculate_completion_percentage(
            len(evaluations), len(questions), early_termination
        )
        
        # Determine readiness category
        readiness_category = self._determine_readiness_category(overall_score)
        
        # Determine hiring readiness
        role_fit = self._calculate_role_fit(candidate, job_requirement, skill_area_scores)
        hiring_readiness = self._determine_hiring_readiness(overall_score, role_fit)
        
        # Generate actionable feedback
        feedback = self._generate_actionable_feedback(
            evaluations, skill_area_scores, job_requirement
        )
        
        # Identify strengths and weaknesses
        strengths = self._identify_overall_strengths(evaluations, skill_area_scores)
        weaknesses = self._identify_overall_weaknesses(evaluations, skill_area_scores)
        
        score = InterviewScore(
            total_score=overall_score,
            skill_area_scores=skill_area_scores,
            question_scores=[e.overall_score for e in evaluations],
            strengths=strengths,
            weaknesses=weaknesses,
            readiness_category=readiness_category,
            hiring_readiness_indicator=hiring_readiness,
            actionable_feedback=feedback,
            estimated_role_fit=role_fit,
            time_management_score=time_management_score,
            adaptability_score=adaptability_score,
            technical_depth=technical_depth,
            communication_quality=communication_quality,
            interview_completion_percentage=completion_percentage,
        )
        
        self.logger.info(f"Interview score calculated: {overall_score}")
        return score
    
    def _group_by_skill_area(self, evaluations: List[AnswerEvaluation],
                            questions: List) -> Dict[SkillArea, List[AnswerEvaluation]]:
        """Group evaluations by skill area."""
        grouped = {}
        
        for skill_area in SkillArea:
            grouped[skill_area] = []
        
        for evaluation in evaluations:
            # Find corresponding question
            question = next((q for q in questions if q.id == evaluation.question_id), None)
            if question:
                grouped[question.skill_area].append(evaluation)
        
        return grouped
    
    def _calculate_skill_area_score(self, skill_area: SkillArea,
                                   evaluations: List[AnswerEvaluation]) -> SkillAreaScore:
        """Calculate score for a specific skill area."""
        if not evaluations:
            return SkillAreaScore(skill_area, 0, 0, 0)
        
        scores = [e.overall_score for e in evaluations]
        average_score = sum(scores) / len(scores)
        
        return SkillAreaScore(
            skill_area=skill_area,
            score=round(average_score, 2),
            questions_asked=len(evaluations),
            average_performance=round(average_score, 2),
        )
    
    def _calculate_overall_score(self, skill_area_scores: Dict[str, SkillAreaScore]) -> float:
        """Calculate overall interview score using weighted average."""
        total_score = 0
        total_weight = 0
        
        for skill_area, weight in self.SKILL_WEIGHTS.items():
            skill_score = skill_area_scores.get(skill_area.value)
            if skill_score:
                total_score += skill_score.score * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return round(total_score / total_weight, 2)
    
    def _calculate_time_management_score(self, evaluations: List[AnswerEvaluation],
                                        questions: List) -> float:
        """Calculate time management score."""
        if not evaluations or not questions:
            return 0.0
        
        time_scores = []
        for evaluation in evaluations:
            question = next((q for q in questions if q.id == evaluation.question_id), None)
            if question:
                time_score = evaluation.time_efficiency_score
                time_scores.append(time_score)
        
        return round(sum(time_scores) / len(time_scores), 2) if time_scores else 0.0
    
    def _calculate_adaptability_score(self, evaluations: List[AnswerEvaluation]) -> float:
        """Calculate adaptability score based on performance variance."""
        if not evaluations or len(evaluations) < 2:
            return 50.0  # Default if insufficient data
        
        scores = [e.overall_score for e in evaluations]
        
        # Calculate score improvement/trend
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        first_avg = sum(first_half) / len(first_half) if first_half else 0
        second_avg = sum(second_half) / len(second_half) if second_half else 0
        
        # Positive improvement is good adaptability
        improvement = (second_avg - first_avg) / max(first_avg, 1)
        
        # Score adaptability: improvements get higher scores, consistency is neutral
        adaptability = 50 + (improvement * 25)  # Scale to 0-100 range
        
        return round(max(min(adaptability, 100), 0), 2)
    
    def _calculate_completion_percentage(self, questions_answered: int,
                                        total_questions: int,
                                        early_termination: bool) -> float:
        """Calculate interview completion percentage."""
        if total_questions == 0:
            return 0.0
        
        percentage = (questions_answered / total_questions) * 100
        
        # Apply penalty for early termination
        if early_termination:
            percentage *= 0.9
        
        return round(percentage, 2)
    
    def _determine_readiness_category(self, overall_score: float) -> str:
        """Determine readiness category based on score."""
        if overall_score >= 75:
            return "Strong"
        elif overall_score >= 60:
            return "Average"
        else:
            return "Needs Improvement"
    
    def _calculate_role_fit(self, candidate: CandidateProfile,
                           job_requirement: JobRequirement,
                           skill_area_scores: Dict[str, SkillAreaScore]) -> float:
        """Calculate role fit score based on candidate and job alignment."""
        fit_score = 0.0
        
        # Check skill alignment
        candidate_skills = set(s.lower() for s in candidate.skills)
        required_skills = set(s.lower() for s in job_requirement.required_skills)
        
        if required_skills:
            skill_match = len(candidate_skills & required_skills) / len(required_skills)
            fit_score += skill_match * 30
        
        # Check technology alignment
        candidate_techs = set(t.lower() for t in candidate.technologies)
        required_techs = set(t.lower() for t in job_requirement.technologies)
        
        if required_techs:
            tech_match = len(candidate_techs & required_techs) / len(required_techs)
            fit_score += tech_match * 25
        
        # Check experience level alignment
        exp_level_match = 1.0
        if candidate.years_of_experience < 2 and job_requirement.experience_level != "entry_level":
            exp_level_match = 0.5
        elif candidate.years_of_experience < 5 and job_requirement.experience_level == "senior_level":
            exp_level_match = 0.7
        
        fit_score += exp_level_match * 20
        
        # Consider interview performance
        technical_score = skill_area_scores.get(SkillArea.TECHNICAL.value)
        if technical_score:
            fit_score += (technical_score.score / 100) * 25
        
        return round(min(fit_score, 100), 2)
    
    def _determine_hiring_readiness(self, overall_score: float, role_fit: float) -> str:
        """Determine hiring readiness indicator."""
        combined_score = (overall_score * 0.6 + role_fit * 0.4)
        
        if combined_score >= 75:
            return "Ready"
        elif combined_score >= 55:
            return "Needs Development"
        else:
            return "Not Ready"
    
    def _generate_actionable_feedback(self, evaluations: List[AnswerEvaluation],
                                     skill_area_scores: Dict[str, SkillAreaScore],
                                     job_requirement: JobRequirement) -> List[str]:
        """Generate actionable feedback for improvement."""
        feedback = []
        
        # Identify weakest skill areas
        weak_areas = sorted(
            [(area, score.score) for area, score in skill_area_scores.items()],
            key=lambda x: x[1]
        )
        
        for area, score in weak_areas[:2]:
            if score < 60:
                feedback.append(f"Improve {area} skills - focus on this area for next interview")
        
        # Identify common weaknesses across evaluations
        all_weaknesses = []
        for eval in evaluations:
            all_weaknesses.extend(eval.areas_for_improvement)
        
        from collections import Counter
        weakness_counts = Counter(all_weaknesses)
        top_weaknesses = weakness_counts.most_common(3)
        
        for weakness, _ in top_weaknesses:
            if "missing" in weakness.lower() or "incomplete" in weakness.lower():
                feedback.append(f"Work on: {weakness}")
        
        # Provide specific technology recommendations
        missed_techs = [t for t in job_requirement.technologies 
                       if not any(t.lower() in eval.answer_text.lower() 
                                 for eval in evaluations)]
        if missed_techs:
            feedback.append(f"Learn more about: {', '.join(missed_techs[:3])}")
        
        # Time management feedback
        time_issues = [e for e in evaluations if e.time_efficiency_score < 50]
        if len(time_issues) >= 2:
            feedback.append("Practice time management - many answers went over time")
        
        # Behavioral feedback
        behavioral_evals = [e for e in evaluations if "behavioral" in e.question_id.lower()]
        if behavioral_evals and behavioral_evals[0].overall_score < 50:
            feedback.append("Prepare stronger behavioral examples - use STAR method")
        
        return feedback
    
    def _identify_overall_strengths(self, evaluations: List[AnswerEvaluation],
                                   skill_area_scores: Dict[str, SkillAreaScore]) -> List[str]:
        """Identify overall interview strengths."""
        strengths = []
        
        # Strong skill areas
        strong_areas = [area for area, score in skill_area_scores.items()
                       if score.score >= 75]
        if strong_areas:
            strengths.append(f"Strong performance in: {', '.join(strong_areas)}")
        
        # Collect individual strengths
        all_strengths = []
        for eval in evaluations:
            all_strengths.extend(eval.strengths)
        
        from collections import Counter
        strength_counts = Counter(all_strengths)
        top_strengths = strength_counts.most_common(3)
        
        for strength, count in top_strengths:
            if count >= 2:
                strengths.append(strength)
        
        # Performance consistency
        scores = [e.overall_score for e in evaluations]
        if scores and max(scores) - min(scores) < 20:
            strengths.append("Consistent performance across questions")
        
        return strengths[:5]
    
    def _identify_overall_weaknesses(self, evaluations: List[AnswerEvaluation],
                                    skill_area_scores: Dict[str, SkillAreaScore]) -> List[str]:
        """Identify overall interview weaknesses."""
        weaknesses = []
        
        # Weak skill areas
        weak_areas = [area for area, score in skill_area_scores.items()
                     if score.score < 50]
        if weak_areas:
            weaknesses.append(f"Needs improvement in: {', '.join(weak_areas)}")
        
        # Collect individual weaknesses
        all_weaknesses = []
        for eval in evaluations:
            all_weaknesses.extend(eval.areas_for_improvement)
        
        from collections import Counter
        weakness_counts = Counter(all_weaknesses)
        top_weaknesses = weakness_counts.most_common(3)
        
        for weakness, count in top_weaknesses:
            if count >= 1:
                weaknesses.append(weakness)
        
        return weaknesses[:4]
    
    def _create_zero_score(self) -> InterviewScore:
        """Create a zero interview score for edge cases."""
        return InterviewScore(
            total_score=0.0,
            skill_area_scores={},
            question_scores=[],
            strengths=[],
            weaknesses=["No data to evaluate"],
            readiness_category="Needs Improvement",
            hiring_readiness_indicator="Not Ready",
            actionable_feedback=["Complete the interview to get evaluation"],
            estimated_role_fit=0.0,
            time_management_score=0.0,
            adaptability_score=0.0,
            technical_depth=0.0,
            communication_quality=0.0,
            interview_completion_percentage=0.0,
        )
