"""Question generator for interview questions."""

import random
from typing import List, Dict, Optional
from src.utils import (
    InterviewQuestion, QuestionDifficulty, SkillArea, 
    CandidateProfile, JobRequirement, get_logger
)

logger = get_logger(__name__)


class QuestionGenerator:
    """Generate interview questions with adaptive difficulty."""
    
    # Question templates for different types and skill areas
    QUESTION_TEMPLATES = {
        SkillArea.TECHNICAL: {
            "easy": [
                "What is {concept} and how would you explain it to a junior developer?",
                "Can you describe the key features of {concept}?",
                "What are the main differences between {concept} and {related_concept}?",
            ],
            "medium": [
                "How would you implement {concept} in a real-world scenario?",
                "What are the pros and cons of using {concept}?",
                "Can you walk us through a situation where you used {concept}?",
            ],
            "hard": [
                "Design a system that uses {concept} to solve {problem}.",
                "What are the performance implications of {concept}?",
                "How would you optimize {concept} for handling large-scale data?",
                "What edge cases might you encounter with {concept}?",
            ],
        },
        SkillArea.PROBLEM_SOLVING: {
            "easy": [
                "Walk me through your approach to solving a {problem}.",
                "What debugging techniques do you typically use?",
                "How do you approach learning a new technology?",
            ],
            "medium": [
                "Design an algorithm to solve {problem}. What's the time complexity?",
                "How would you optimize this solution for performance?",
                "Can you think of edge cases for this problem?",
            ],
            "hard": [
                "Design a scalable solution for {problem} that handles millions of operations.",
                "How would you balance {tradeoff1} vs {tradeoff2} in this solution?",
                "What would be your strategy for this complex problem?",
            ],
        },
        SkillArea.BEHAVIORAL: {
            "easy": [
                "Tell me about a time when you successfully completed a project.",
                "How do you handle feedback from colleagues?",
                "Describe your ideal work environment.",
            ],
            "medium": [
                "Tell me about a conflict with a team member and how you resolved it.",
                "Share an experience where you had to learn quickly.",
                "Describe a time when you took initiative on a project.",
            ],
            "hard": [
                "Tell me about your biggest failure and what you learned from it.",
                "Describe a time when you had to make a difficult decision.",
                "Share an experience where you influenced a major decision.",
            ],
        },
        SkillArea.COMMUNICATION: {
            "easy": [
                "How would you explain {concept} to a non-technical stakeholder?",
                "Tell me about a time you documented your work.",
            ],
            "medium": [
                "How do you handle presenting complex ideas to different audiences?",
                "Describe your approach to technical documentation.",
            ],
            "hard": [
                "Tell me about a time you had to convince stakeholders of a technical decision.",
                "How do you handle disagreement with senior team members?",
            ],
        },
        SkillArea.SYSTEM_DESIGN: {
            "easy": [
                "Describe the architecture of a {system}.",
                "What are the components needed for {system}?",
            ],
            "medium": [
                "Design a scalable {system} for 1M concurrent users.",
                "How would you handle data consistency in {system}?",
            ],
            "hard": [
                "Design a global {system} across multiple regions with disaster recovery.",
                "How would you optimize {system} for both latency and throughput?",
            ],
        },
    }
    
    CONCEPTS = {
        "technical": ["REST API", "Database Indexing", "Caching", "Microservices",
                     "Load Balancing", "Message Queues", "Containerization", 
                     "CI/CD", "Event Streaming", "Distributed Systems"],
        "system_design": ["URL Shortener", "Social Media Feed", "Chat System",
                         "Video Streaming Platform", "E-commerce Platform",
                         "Real-time Analytics", "Recommendation Engine"],
        "problems": ["Data Processing", "Performance Optimization", "Scalability",
                    "Reliability", "Security", "Resource Management"],
    }
    
    def __init__(self):
        """Initialize the question generator."""
        self.logger = logger
        self.generated_questions: Dict[str, InterviewQuestion] = {}
        self.question_counter = 0
    
    def generate_questions(self, candidate: CandidateProfile,
                         job_requirement: JobRequirement,
                         num_questions: int = 5) -> List[InterviewQuestion]:
        """
        Generate interview questions based on candidate and job requirements.
        
        Args:
            candidate: Candidate profile
            job_requirement: Job requirements
            num_questions: Number of questions to generate
            
        Returns:
            List of interview questions with adaptive difficulty
        """
        self.logger.info(f"Generating {num_questions} interview questions")
        
        questions = []
        skill_areas = [SkillArea.TECHNICAL, SkillArea.PROBLEM_SOLVING,
                      SkillArea.BEHAVIORAL, SkillArea.COMMUNICATION,
                      SkillArea.SYSTEM_DESIGN]
        
        # Distribute questions across skill areas
        questions_per_area = num_questions // len(skill_areas)
        remaining = num_questions % len(skill_areas)
        
        difficulty_progression = self._create_difficulty_progression(num_questions)
        
        question_id = 0
        for area_idx, skill_area in enumerate(skill_areas):
            area_count = questions_per_area + (1 if area_idx < remaining else 0)
            
            for i in range(area_count):
                difficulty = difficulty_progression[question_id]
                question = self._generate_question(
                    skill_area, difficulty, candidate, job_requirement
                )
                questions.append(question)
                self.generated_questions[question.id] = question
                question_id += 1
        
        self.logger.info(f"Generated {len(questions)} questions successfully")
        return questions
    
    def adapt_difficulty(self, current_score: float, next_question: InterviewQuestion) -> InterviewQuestion:
        """
        Adapt question difficulty based on previous answer performance.
        
        Args:
            current_score: Score from previous answer (0-100)
            next_question: Current next question
            
        Returns:
            Adjusted question with new difficulty level
        """
        new_difficulty = next_question.difficulty
        
        if current_score >= 80:
            # Increase difficulty
            if new_difficulty == QuestionDifficulty.EASY:
                new_difficulty = QuestionDifficulty.MEDIUM
            elif new_difficulty == QuestionDifficulty.MEDIUM:
                new_difficulty = QuestionDifficulty.HARD
        elif current_score < 50:
            # Decrease difficulty
            if new_difficulty == QuestionDifficulty.HARD:
                new_difficulty = QuestionDifficulty.MEDIUM
            elif new_difficulty == QuestionDifficulty.MEDIUM:
                new_difficulty = QuestionDifficulty.EASY
        
        self.logger.info(f"Adapted question difficulty from {next_question.difficulty} to {new_difficulty}")
        
        return self._regenerate_question(next_question, new_difficulty)
    
    def _generate_question(self, skill_area: SkillArea, difficulty: QuestionDifficulty,
                         candidate: CandidateProfile,
                         job_requirement: JobRequirement) -> InterviewQuestion:
        """Generate a single interview question."""
        self.question_counter += 1
        question_id = f"Q_{skill_area.value}_{difficulty.value}_{self.question_counter}"
        
        # Select question template
        templates = self.QUESTION_TEMPLATES.get(skill_area, {}).get(difficulty.value, [])
        if not templates:
            templates = self.QUESTION_TEMPLATES[SkillArea.TECHNICAL][difficulty.value]
        
        template = random.choice(templates)
        
        # Select concepts/topics relevant to job
        relevant_techs = [t for t in job_requirement.technologies 
                         if t in candidate.technologies]
        topics = relevant_techs or job_requirement.technologies[:3]
        topic = random.choice(topics) if topics else "Python"
        
        # Format question
        question_text = template.format(
            concept=topic,
            related_concept=random.choice(job_requirement.technologies),
            problem=random.choice(self.CONCEPTS["problems"]),
            system=random.choice(self.CONCEPTS["system_design"]),
            tradeoff1=random.choice(["latency", "throughput", "consistency"]),
            tradeoff2=random.choice(["availability", "partition tolerance", "cost"]),
        )
        
        # Determine question type
        question_type = self._determine_question_type(skill_area)
        
        # Extract expected concepts and answer points
        expected_concepts = self._extract_expected_concepts(skill_area, topic)
        ideal_answer_points = self._generate_ideal_answer_points(question_text, skill_area)
        
        return InterviewQuestion(
            id=question_id,
            question_text=question_text,
            difficulty=difficulty,
            skill_area=skill_area,
            question_type=question_type,
            expected_concepts=expected_concepts,
            ideal_answer_points=ideal_answer_points,
            time_limit=120 if difficulty == QuestionDifficulty.EASY else 
                      180 if difficulty == QuestionDifficulty.MEDIUM else 240,
        )
    
    def _regenerate_question(self, original: InterviewQuestion,
                            new_difficulty: QuestionDifficulty) -> InterviewQuestion:
        """Regenerate question with new difficulty level."""
        self.question_counter += 1
        question_id = f"Q_{original.skill_area.value}_{new_difficulty.value}_{self.question_counter}"
        
        templates = self.QUESTION_TEMPLATES[original.skill_area][new_difficulty.value]
        template = random.choice(templates)
        
        # Extract concepts from original question
        concepts = original.expected_concepts
        topic = concepts[0] if concepts else "Technology"
        
        question_text = template.format(
            concept=topic,
            related_concept=random.choice(concepts + ["Advanced Topic"]),
            problem=random.choice(self.CONCEPTS["problems"]),
            system=random.choice(self.CONCEPTS["system_design"]),
            tradeoff1=random.choice(["latency", "throughput", "consistency"]),
            tradeoff2=random.choice(["availability", "partition tolerance", "cost"]),
        )
        
        return InterviewQuestion(
            id=question_id,
            question_text=question_text,
            difficulty=new_difficulty,
            skill_area=original.skill_area,
            question_type=original.question_type,
            expected_concepts=original.expected_concepts,
            ideal_answer_points=self._generate_ideal_answer_points(question_text, original.skill_area),
            time_limit=120 if new_difficulty == QuestionDifficulty.EASY else
                      180 if new_difficulty == QuestionDifficulty.MEDIUM else 240,
        )
    
    def _create_difficulty_progression(self, num_questions: int) -> List[QuestionDifficulty]:
        """Create a difficulty progression for questions."""
        progression = []
        
        # Start easier, progress to harder
        for i in range(num_questions):
            ratio = i / max(num_questions - 1, 1)
            
            if ratio < 0.3:
                progression.append(QuestionDifficulty.EASY)
            elif ratio < 0.7:
                progression.append(QuestionDifficulty.MEDIUM)
            else:
                progression.append(QuestionDifficulty.HARD)
        
        return progression
    
    def _determine_question_type(self, skill_area: SkillArea) -> str:
        """Determine question type based on skill area."""
        type_map = {
            SkillArea.TECHNICAL: "technical",
            SkillArea.PROBLEM_SOLVING: "problem-solving",
            SkillArea.BEHAVIORAL: "behavioral",
            SkillArea.COMMUNICATION: "communication",
            SkillArea.SYSTEM_DESIGN: "scenario-based",
        }
        return type_map.get(skill_area, "conceptual")
    
    def _extract_expected_concepts(self, skill_area: SkillArea, topic: str) -> List[str]:
        """Extract expected concepts for the question."""
        if skill_area == SkillArea.TECHNICAL:
            return [topic, "Architecture", "Implementation", "Best Practices"]
        elif skill_area == SkillArea.PROBLEM_SOLVING:
            return ["Algorithm", "Complexity Analysis", "Optimization", "Edge Cases"]
        elif skill_area == SkillArea.BEHAVIORAL:
            return ["Teamwork", "Communication", "Problem Resolution", "Initiative"]
        elif skill_area == SkillArea.SYSTEM_DESIGN:
            return ["Scalability", "Reliability", "Performance", "Cost"]
        else:
            return ["Clarity", "Depth", "Relevance", "Examples"]
    
    def _generate_ideal_answer_points(self, question: str, skill_area: SkillArea) -> List[str]:
        """Generate ideal answer points for the question."""
        if skill_area == SkillArea.TECHNICAL:
            return ["Clear definition", "Use cases", "Advantages and disadvantages",
                   "Examples", "Best practices", "Common pitfalls"]
        elif skill_area == SkillArea.PROBLEM_SOLVING:
            return ["Understand the problem", "Propose approach", "Discuss complexity",
                   "Consider edge cases", "Explain optimization", "Code or pseudocode"]
        elif skill_area == SkillArea.BEHAVIORAL:
            return ["Specific situation", "Your role", "Actions taken", "Results",
                   "Lessons learned", "Apply to current role"]
        elif skill_area == SkillArea.SYSTEM_DESIGN:
            return ["Requirements analysis", "Architecture design", "Technology choices",
                   "Scalability plan", "Failure handling", "Cost optimization"]
        else:
            return ["Direct answer", "Supporting examples", "Clear explanation",
                   "Relevant details", "Thoughtful conclusion"]
