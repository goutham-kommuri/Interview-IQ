"""Answer evaluator for assessing candidate responses."""

import re
from typing import List, Dict, Tuple
from src.utils import (
    AnswerEvaluation, InterviewQuestion, SkillArea, get_logger
)

logger = get_logger(__name__)


class AnswerEvaluator:
    """Evaluate candidate answers against expected criteria."""
    
    # Scoring weights for different evaluation factors
    SCORE_WEIGHTS = {
        "accuracy": 0.25,
        "clarity": 0.20,
        "depth": 0.25,
        "relevance": 0.20,
        "time_efficiency": 0.10,
    }
    
    # Keywords for evaluation
    QUALITY_KEYWORDS = {
        "positive": ["clear", "correct", "accurate", "complete", "relevant",
                    "concise", "well-structured", "thoughtful", "innovative"],
        "negative": ["unclear", "incorrect", "incomplete", "irrelevant", "verbose",
                    "confused", "missing", "weak", "superficial"],
    }
    
    def __init__(self):
        """Initialize the answer evaluator."""
        self.logger = logger
    
    def evaluate(self, question: InterviewQuestion, answer: str,
                time_taken: int) -> AnswerEvaluation:
        """
        Evaluate a candidate's answer to a question.
        
        Args:
            question: Interview question
            answer: Candidate's answer
            time_taken: Time taken to answer (seconds)
            
        Returns:
            AnswerEvaluation with detailed scoring
        """
        self.logger.info(f"Evaluating answer for question: {question.id}")
        
        # Calculate individual scores
        accuracy_score = self._evaluate_accuracy(question, answer)
        clarity_score = self._evaluate_clarity(answer)
        depth_score = self._evaluate_depth(answer, question)
        relevance_score = self._evaluate_relevance(answer, question)
        time_efficiency_score = self._evaluate_time_efficiency(time_taken, question.time_limit)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(
            accuracy_score, clarity_score, depth_score,
            relevance_score, time_efficiency_score
        )
        
        # Generate feedback
        feedback = self._generate_feedback(
            accuracy_score, clarity_score, depth_score,
            relevance_score, time_efficiency_score
        )
        
        # Extract key information
        strengths = self._identify_strengths(answer, question)
        areas_for_improvement = self._identify_weaknesses(answer, question)
        key_points = self._extract_key_points(answer, question)
        missed_concepts = self._identify_missed_concepts(answer, question)
        
        evaluation = AnswerEvaluation(
            question_id=question.id,
            answer_text=answer,
            time_taken=time_taken,
            accuracy_score=accuracy_score,
            clarity_score=clarity_score,
            depth_score=depth_score,
            relevance_score=relevance_score,
            time_efficiency_score=time_efficiency_score,
            overall_score=overall_score,
            feedback=feedback,
            strengths=strengths,
            areas_for_improvement=areas_for_improvement,
            key_points_covered=key_points,
            missed_concepts=missed_concepts,
        )
        
        self.logger.info(f"Evaluation complete. Overall score: {overall_score}")
        return evaluation
    
    def _evaluate_accuracy(self, question: InterviewQuestion, answer: str) -> float:
        """Evaluate accuracy of the answer."""
        if not answer or len(answer.strip()) < 10:
            return 0.0
        
        score = 50.0  # Base score
        answer_lower = answer.lower()
        
        # Check for key concepts mentioned
        concepts_found = 0
        for concept in question.expected_concepts:
            if concept.lower() in answer_lower:
                concepts_found += 1
        
        if len(question.expected_concepts) > 0:
            concept_coverage = concepts_found / len(question.expected_concepts)
            score += concept_coverage * 30.0  # Up to 30 points for concepts
        
        # Check for technical correctness indicators
        if question.skill_area == SkillArea.TECHNICAL:
            correctness_patterns = [
                r"correct", r"accurate", r"right", r"proper",
                r"works", r"solution", r"approach"
            ]
            pattern_matches = sum(1 for pattern in correctness_patterns 
                                if re.search(pattern, answer_lower))
            score += min(pattern_matches * 5, 20)
        
        return min(score, 100.0)
    
    def _evaluate_clarity(self, answer: str) -> float:
        """Evaluate clarity of the answer."""
        if not answer:
            return 0.0
        
        score = 50.0  # Base score
        
        # Sentence length and structure
        sentences = [s.strip() for s in answer.split('.') if s.strip()]
        if not sentences:
            return 20.0
        
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Optimal sentence length is 15-25 words
        if 15 <= avg_sentence_length <= 25:
            score += 20.0
        elif avg_sentence_length > 35:  # Too long and complex
            score -= 10.0
        elif avg_sentence_length < 5:  # Too short and choppy
            score -= 5.0
        
        # Check for clarity indicators
        clarity_patterns = [
            r"i think", r"in my opinion", r"for example", r"specifically",
            r"first", r"second", r"finally", r"therefore"
        ]
        pattern_matches = sum(1 for pattern in clarity_patterns 
                            if re.search(pattern, answer.lower()))
        score += min(pattern_matches * 5, 15)
        
        # Check for confusing phrases
        confusing_patterns = [
            r"i don't know", r"maybe", r"probably", r"kinda",
            r"sort of", r"umm", r"uh", r"like"
        ]
        confusing_count = sum(1 for pattern in confusing_patterns 
                            if re.search(pattern, answer.lower()))
        score -= min(confusing_count * 10, 25)
        
        return max(min(score, 100.0), 0.0)
    
    def _evaluate_depth(self, answer: str, question: InterviewQuestion) -> float:
        """Evaluate depth of the answer."""
        if not answer:
            return 0.0
        
        score = 50.0  # Base score
        
        # Answer length (more comprehensive answers tend to be longer)
        word_count = len(answer.split())
        
        # Expected word count based on difficulty
        expected_words = {
            "easy": 100,
            "medium": 200,
            "hard": 300,
        }
        expected = expected_words.get(question.difficulty.value, 200)
        
        if word_count >= expected:
            score += 20.0
        elif word_count >= expected * 0.7:
            score += 10.0
        elif word_count >= expected * 0.4:
            score += 5.0
        else:
            score -= 10.0
        
        # Check for depth indicators
        depth_patterns = [
            r"furthermore", r"moreover", r"additionally", r"in detail",
            r"example", r"specifically", r"consider", r"analyze"
        ]
        pattern_matches = sum(1 for pattern in depth_patterns 
                            if re.search(pattern, answer.lower()))
        score += min(pattern_matches * 5, 20)
        
        # Check for multiple aspects covered
        aspect_count = len([p for p in question.ideal_answer_points 
                          if any(word.lower() in answer.lower() 
                                for word in p.lower().split())])
        score += min(aspect_count * 5, 15)
        
        return max(min(score, 100.0), 0.0)
    
    def _evaluate_relevance(self, answer: str, question: InterviewQuestion) -> float:
        """Evaluate relevance of the answer to the question."""
        if not answer:
            return 0.0
        
        score = 50.0  # Base score
        answer_lower = answer.lower()
        
        # Check if answer addresses the question directly
        question_words = set(word.lower() for word in question.question_text.split() 
                           if len(word) > 3)
        answer_words = set(word.lower() for word in answer.split() if len(word) > 3)
        
        word_overlap = len(question_words & answer_words) / max(len(question_words), 1)
        score += word_overlap * 30  # Up to 30 points
        
        # Check for ideal answer points mentioned
        ideal_points_coverage = 0
        for point in question.ideal_answer_points:
            if any(keyword.lower() in answer_lower 
                  for keyword in point.lower().split()):
                ideal_points_coverage += 1
        
        if len(question.ideal_answer_points) > 0:
            coverage_score = ideal_points_coverage / len(question.ideal_answer_points)
            score += coverage_score * 20  # Up to 20 points
        
        return min(score, 100.0)
    
    def _evaluate_time_efficiency(self, time_taken: int, time_limit: int) -> float:
        """Evaluate time efficiency of the answer."""
        if time_taken <= 0:
            return 0.0
        
        # Optimal time is 70-90% of limit
        optimal_time_min = time_limit * 0.7
        optimal_time_max = time_limit * 0.9
        
        if optimal_time_min <= time_taken <= optimal_time_max:
            return 100.0
        elif time_taken < optimal_time_min:
            # Too quick - might be incomplete
            return max(50 + (time_taken / optimal_time_min - 0.5) * 100, 50.0)
        else:
            # Overtime penalty
            overtime_ratio = (time_taken - time_limit) / time_limit
            return max(100 - overtime_ratio * 50, 0.0)
    
    def _calculate_overall_score(self, accuracy: float, clarity: float,
                                depth: float, relevance: float,
                                time_efficiency: float) -> float:
        """Calculate overall score using weighted average."""
        score = (
            accuracy * self.SCORE_WEIGHTS["accuracy"] +
            clarity * self.SCORE_WEIGHTS["clarity"] +
            depth * self.SCORE_WEIGHTS["depth"] +
            relevance * self.SCORE_WEIGHTS["relevance"] +
            time_efficiency * self.SCORE_WEIGHTS["time_efficiency"]
        )
        return round(score, 2)
    
    def _generate_feedback(self, accuracy: float, clarity: float, depth: float,
                         relevance: float, time_efficiency: float) -> str:
        """Generate feedback based on evaluation scores."""
        feedback_parts = []
        
        scores = {
            "Accuracy": accuracy,
            "Clarity": clarity,
            "Depth": depth,
            "Relevance": relevance,
            "Time Management": time_efficiency,
        }
        
        for aspect, score in scores.items():
            if score >= 80:
                feedback_parts.append(f"{aspect}: Excellent - Well done! ✓")
            elif score >= 60:
                feedback_parts.append(f"{aspect}: Good - Solid response.")
            elif score >= 40:
                feedback_parts.append(f"{aspect}: Fair - Room for improvement.")
            else:
                feedback_parts.append(f"{aspect}: Needs Improvement - Focus here.")
        
        return "\n".join(feedback_parts)
    
    def _identify_strengths(self, answer: str, question: InterviewQuestion) -> List[str]:
        """Identify strengths in the answer."""
        strengths = []
        answer_lower = answer.lower()
        
        if len(answer) > 150:
            strengths.append("Comprehensive answer with good detail")
        
        if any(pattern in answer_lower for pattern in 
               ["for example", "specifically", "such as"]):
            strengths.append("Provided specific examples")
        
        if any(keyword in answer_lower for keyword in question.expected_concepts):
            strengths.append("Covered key concepts well")
        
        if len([s for s in answer.split('.') if s.strip()]) >= 3:
            strengths.append("Well-structured response")
        
        return strengths
    
    def _identify_weaknesses(self, answer: str, question: InterviewQuestion) -> List[str]:
        """Identify weaknesses in the answer."""
        weaknesses = []
        answer_lower = answer.lower()
        
        if len(answer) < 50:
            weaknesses.append("Answer too brief - consider providing more detail")
        
        if any(pattern in answer_lower for pattern in 
               ["i don't know", "not sure", "maybe", "probably"]):
            weaknesses.append("Uncertain language - be more confident")
        
        missing_concepts = [c for c in question.expected_concepts 
                           if c.lower() not in answer_lower]
        if missing_concepts:
            weaknesses.append(f"Missing key concepts: {', '.join(missing_concepts[:2])}")
        
        if len([s for s in answer.split('.') if s.strip()]) < 2:
            weaknesses.append("Could structure the response better")
        
        return weaknesses
    
    def _extract_key_points(self, answer: str, question: InterviewQuestion) -> List[str]:
        """Extract key points covered in the answer."""
        key_points = []
        answer_lower = answer.lower()
        
        for point in question.ideal_answer_points:
            if any(keyword.lower() in answer_lower for keyword in point.lower().split()):
                key_points.append(point)
        
        return key_points
    
    def _identify_missed_concepts(self, answer: str, 
                                 question: InterviewQuestion) -> List[str]:
        """Identify concepts that were expected but missed."""
        missed = []
        answer_lower = answer.lower()
        
        for concept in question.expected_concepts:
            if concept.lower() not in answer_lower:
                missed.append(concept)
        
        return missed
