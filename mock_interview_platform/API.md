# API Documentation - AI-Powered Mock Interview Platform

## Overview

The AI-Powered Mock Interview Platform provides a comprehensive API for conducting intelligent mock interviews with objective evaluation and adaptive difficulty.

## Table of Contents

1. [Core Classes](#core-classes)
2. [Data Models](#data-models)
3. [API Methods](#api-methods)
4. [Usage Examples](#usage-examples)
5. [Error Handling](#error-handling)

---

## Core Classes

### AIInterviewer

The main agent class that orchestrates the entire interview process.

#### Initialization

```python
from src.agents import AIInterviewer
from src.utils import Config

config = Config()
interviewer = AIInterviewer(config)
```

#### Methods

##### initialize_interview()

Initialize an interview session with resume and job description.

```python
def initialize_interview(
    resume_text: str,
    jd_text: str,
    candidate_name: str = "Candidate",
    job_title: str = "Tech Position"
) -> Dict[str, Any]
```

**Parameters:**
- `resume_text` (str): Candidate's resume in text format
- `jd_text` (str): Job description in text format
- `candidate_name` (str): Name of the candidate
- `job_title` (str): Title of the job position

**Returns:**
```python
{
    "status": "success" | "error",
    "message": str,
    "candidate_name": str,
    "job_title": str,
    "total_questions": int,
    "skill_gaps": List[str],
    "first_question": str
}
```

**Example:**
```python
result = interviewer.initialize_interview(
    resume_text=resume,
    jd_text=job_description,
    candidate_name="Alice Johnson",
    job_title="Senior Backend Engineer"
)

if result["status"] == "success":
    print(f"Questions: {result['total_questions']}")
    print(f"Skill Gaps: {result['skill_gaps']}")
```

---

##### get_current_question()

Get the current interview question.

```python
def get_current_question() -> Optional[Dict[str, Any]]
```

**Returns:**
```python
{
    "question_number": int,           # Current question number (1-indexed)
    "total_questions": int,           # Total questions in interview
    "question_id": str,               # Unique question identifier
    "question_text": str,             # The actual question
    "difficulty": str,                # "easy" | "medium" | "hard"
    "skill_area": str,                # Skill area being assessed
    "time_limit": int,                # Time limit in seconds
    "question_type": str              # Type: technical, behavioral, etc.
} | None
```

**Example:**
```python
question = interviewer.get_current_question()

if question:
    print(f"Q{question['question_number']}: {question['question_text']}")
    print(f"Difficulty: {question['difficulty']}")
    print(f"Time limit: {question['time_limit']} seconds")
else:
    print("No more questions")
```

---

##### evaluate_answer()

Evaluate candidate's answer to current question.

```python
def evaluate_answer(
    answer_text: str,
    time_taken: int
) -> Dict[str, Any]
```

**Parameters:**
- `answer_text` (str): Candidate's answer
- `time_taken` (int): Time taken to answer in seconds

**Returns:**
```python
{
    "status": "success" | "error",
    "overall_score": float,           # 0-100
    "accuracy": float,                # 0-100
    "clarity": float,                 # 0-100
    "depth": float,                   # 0-100
    "relevance": float,               # 0-100
    "time_efficiency": float,         # 0-100
    "feedback": str,                  # Detailed feedback
    "strengths": List[str],           # Identified strengths
    "areas_for_improvement": List[str],
    "key_points_covered": List[str],
    "missed_concepts": List[str],
    "interview_continues": bool,      # Whether to continue
    "next_question": Dict | None      # Next question if available
}
```

**Example:**
```python
# Get answer from candidate
answer = "Based on my understanding, I would..."
time_taken = 145  # seconds

# Evaluate
result = interviewer.evaluate_answer(answer, time_taken)

print(f"Score: {result['overall_score']}/100")
print(f"Accuracy: {result['accuracy']}/100")
print(f"Feedback: {result['feedback']}")

if result['interview_continues']:
    next_q = result['next_question']
    print(f"Next question: {next_q['question_text']}")
```

---

##### conclude_interview()

Conclude the interview and generate final score.

```python
def conclude_interview() -> InterviewScore
```

**Returns:** `InterviewScore` object (see Data Models)

**Example:**
```python
final_score = interviewer.conclude_interview()

print(f"Final Score: {final_score.total_score}/100")
print(f"Readiness: {final_score.readiness_category}")
print(f"Hiring Ready: {final_score.hiring_readiness_indicator}")
print(f"Role Fit: {final_score.estimated_role_fit}%")
```

---

##### generate_interview_report()

Generate detailed interview report as string.

```python
def generate_interview_report() -> str
```

**Returns:** Formatted interview report string

**Example:**
```python
report = interviewer.generate_interview_report()
print(report)

# Or save to file
with open("interview_report.txt", "w") as f:
    f.write(report)
```

---

### ResumeAnalyzer

Analyzes resume and extracts candidate information.

```python
from src.core import ResumeAnalyzer

analyzer = ResumeAnalyzer()
profile = analyzer.analyze(resume_text, candidate_name="John Doe")
```

**Returns:** `CandidateProfile` object

---

### JobDescriptionAnalyzer

Analyzes job description and extracts requirements.

```python
from src.core import JobDescriptionAnalyzer

analyzer = JobDescriptionAnalyzer()
requirement = analyzer.analyze(jd_text, job_title="Senior Engineer")

# Identify skill gaps
gaps = analyzer.identify_skill_gaps(candidate_profile, requirement)
```

**Returns:** `JobRequirement` object, `List[str]` for skill gaps

---

### QuestionGenerator

Generates interview questions with adaptive difficulty.

```python
from src.core import QuestionGenerator

generator = QuestionGenerator()

# Generate questions
questions = generator.generate_questions(
    candidate=candidate_profile,
    job_requirement=job_requirement,
    num_questions=5
)

# Adapt difficulty based on performance
adapted_question = generator.adapt_difficulty(
    current_score=85,
    next_question=questions[1]
)
```

---

### AnswerEvaluator

Evaluates candidate answers with detailed scoring.

```python
from src.core import AnswerEvaluator

evaluator = AnswerEvaluator()

evaluation = evaluator.evaluate(
    question=question,
    answer="The candidate's answer...",
    time_taken=120
)

print(f"Score: {evaluation.overall_score}")
print(f"Strengths: {evaluation.strengths}")
```

**Returns:** `AnswerEvaluation` object

---

### InterviewScorer

Calculates final interview score and generates feedback.

```python
from src.core import InterviewScorer

scorer = InterviewScorer()

final_score = scorer.calculate_score(
    evaluations=evaluations,
    job_requirement=job_requirement,
    candidate=candidate_profile,
    questions=questions,
    early_termination=False
)

print(f"Final Score: {final_score.total_score}/100")
print(f"Strengths: {final_score.strengths}")
print(f"Feedback: {final_score.actionable_feedback}")
```

**Returns:** `InterviewScore` object

---

## Data Models

### CandidateProfile

```python
@dataclass
class CandidateProfile:
    name: str                          # Candidate name
    email: str                         # Email address
    phone: str                         # Phone number
    years_of_experience: int           # Years of experience
    skills: List[str]                  # Technical and soft skills
    technologies: List[str]            # Technology stack
    projects: List[Dict[str, str]]     # Projects list
    education: List[Dict[str, str]]    # Education
    certifications: List[str]          # Certifications
    summary: str                       # Professional summary
    strengths: List[str]               # Identified strengths
```

---

### JobRequirement

```python
@dataclass
class JobRequirement:
    title: str                         # Job title
    required_skills: List[str]         # Required skills
    preferred_skills: List[str]        # Preferred skills
    technologies: List[str]            # Required technologies
    experience_level: str              # Level: entry_level, mid_level, senior_level
    key_responsibilities: List[str]    # Main responsibilities
    nice_to_have: List[str]           # Nice-to-have items
    role_description: str              # Job description summary
    skill_gaps: List[str]              # Skill gaps (computed)
```

---

### InterviewQuestion

```python
@dataclass
class InterviewQuestion:
    id: str                            # Unique question ID
    question_text: str                 # The question
    difficulty: QuestionDifficulty     # easy, medium, hard
    skill_area: SkillArea              # Skill area
    question_type: str                 # Type: technical, behavioral, etc.
    expected_concepts: List[str]       # Expected key concepts
    ideal_answer_points: List[str]     # Ideal answer points
    time_limit: int                    # Time limit in seconds
```

---

### AnswerEvaluation

```python
@dataclass
class AnswerEvaluation:
    question_id: str                   # Question ID
    answer_text: str                   # Candidate's answer
    time_taken: int                    # Time taken (seconds)
    accuracy_score: float              # 0-100
    clarity_score: float               # 0-100
    depth_score: float                 # 0-100
    relevance_score: float             # 0-100
    time_efficiency_score: float       # 0-100
    overall_score: float               # 0-100 (weighted average)
    feedback: str                      # Detailed feedback
    strengths: List[str]               # Answer strengths
    areas_for_improvement: List[str]   # Areas to improve
    key_points_covered: List[str]      # Key points mentioned
    missed_concepts: List[str]         # Missed concepts
```

---

### InterviewScore

```python
@dataclass
class InterviewScore:
    total_score: float                 # Final score (0-100)
    skill_area_scores: Dict[str, SkillAreaScore]  # Breakdown by skill
    question_scores: List[float]       # Individual question scores
    strengths: List[str]               # Top strengths
    weaknesses: List[str]              # Top weaknesses
    readiness_category: str            # Strong, Average, Needs Improvement
    hiring_readiness_indicator: str    # Ready, Needs Development, Not Ready
    actionable_feedback: List[str]     # Specific recommendations
    estimated_role_fit: float          # % role fit (0-100)
    time_management_score: float       # 0-100
    adaptability_score: float          # 0-100
    technical_depth: float             # 0-100
    communication_quality: float       # 0-100
    interview_completion_percentage: float  # 0-100
```

---

### QuestionDifficulty (Enum)

```python
class QuestionDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
```

---

### SkillArea (Enum)

```python
class SkillArea(str, Enum):
    TECHNICAL = "technical"
    PROBLEM_SOLVING = "problem_solving"
    COMMUNICATION = "communication"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"
```

---

## API Methods

### Complete Interview Flow

```python
from src.agents import AIInterviewer
from src.utils import Config

# 1. Initialize
config = Config()
interviewer = AIInterviewer(config)

init_result = interviewer.initialize_interview(
    resume_text=resume,
    jd_text=job_description,
    candidate_name="Jane Doe",
    job_title="Software Engineer"
)

if init_result["status"] != "success":
    raise Exception(init_result["message"])

# 2. Interview loop
while True:
    # Get current question
    question = interviewer.get_current_question()
    if not question:
        break
    
    # Display and collect answer
    print(f"\nQuestion {question['question_number']}: {question['question_text']}")
    answer = input("Your answer: ")
    time_taken = int(input("Time taken (seconds): "))
    
    # Evaluate
    result = interviewer.evaluate_answer(answer, time_taken)
    
    print(f"\nScore: {result['overall_score']}/100")
    print(f"Feedback: {result['feedback']}")
    
    # Check if continues
    if not result['interview_continues']:
        break

# 3. Conclude
final_score = interviewer.conclude_interview()

# 4. Report
report = interviewer.generate_interview_report()
print(report)
```

---

## Usage Examples

### Example 1: Basic Interview

```python
from src.agents import AIInterviewer
from src.utils import Config

config = Config()
interviewer = AIInterviewer(config)

# Initialize
interviewer.initialize_interview(resume, jd, "Alice", "Engineer")

# Get first question
q = interviewer.get_current_question()
print(q['question_text'])

# Answer and evaluate
result = interviewer.evaluate_answer("My answer is...", 150)
print(f"Score: {result['overall_score']}")

# Continue with more questions...
# Get final score
score = interviewer.conclude_interview()
print(f"Final: {score.total_score}/100")
```

---

### Example 2: Analyze Candidate and Role

```python
from src.core import ResumeAnalyzer, JobDescriptionAnalyzer

resume_analyzer = ResumeAnalyzer()
jd_analyzer = JobDescriptionAnalyzer()

# Analyze
candidate = resume_analyzer.analyze(resume_text)
job = jd_analyzer.analyze(jd_text)

# Find gaps
gaps = jd_analyzer.identify_skill_gaps(candidate, job)

print(f"Candidate: {candidate.name}")
print(f"Skills: {candidate.skills}")
print(f"Skill Gaps: {gaps}")
```

---

### Example 3: Generate Custom Questions

```python
from src.core import QuestionGenerator
from src.utils import QuestionDifficulty, SkillArea

generator = QuestionGenerator()

# Generate for specific skill area
questions = generator.generate_questions(
    candidate=candidate_profile,
    job_requirement=job_requirement,
    num_questions=3
)

# Adapt based on performance
if avg_score > 80:
    harder_q = generator.adapt_difficulty(85, questions[1])
    print(f"Harder question: {harder_q.question_text}")
```

---

### Example 4: Detailed Evaluation

```python
from src.core import AnswerEvaluator

evaluator = AnswerEvaluator()

eval = evaluator.evaluate(question, answer_text, time_taken)

print(f"Overall: {eval.overall_score}/100")
print(f"Accuracy: {eval.accuracy_score}")
print(f"Clarity: {eval.clarity_score}")
print(f"Depth: {eval.depth_score}")
print(f"Relevance: {eval.relevance_score}")
print(f"Time: {eval.time_efficiency_score}")
print(f"\nStrengths:")
for s in eval.strengths:
    print(f"  ✓ {s}")
print(f"\nAreas to improve:")
for a in eval.areas_for_improvement:
    print(f"  ✗ {a}")
```

---

## Error Handling

### Common Errors

```python
# Initialize error
try:
    result = interviewer.initialize_interview(resume, jd)
    if result["status"] == "error":
        print(f"Error: {result['message']}")
except Exception as e:
    print(f"Exception: {e}")

# No active question
question = interviewer.get_current_question()
if not question:
    print("Interview finished")

# Evaluation error
try:
    result = interviewer.evaluate_answer(answer, time)
    if result["status"] == "error":
        print(f"Evaluation error: {result['message']}")
except Exception as e:
    print(f"Exception: {e}")
```

---

## Configuration

```python
from src.utils import Config

config = Config()

# Model settings
print(config.use_foundry)              # True if using Foundry
print(config.foundry_api_key)
print(config.github_token)

# Interview settings
print(config.max_questions)            # Default: 5
print(config.time_per_question)        # Default: 120 seconds
print(config.passing_threshold)        # Default: 60%
print(config.early_termination_threshold)  # Default: 40%

# Get model config
model_cfg = config.model_config
print(model_cfg)
```

---

## Enums and Constants

### QuestionDifficulty
- `EASY`: Basic concepts, definitions
- `MEDIUM`: Real-world scenarios
- `HARD`: Complex design, optimization

### SkillArea
- `TECHNICAL`: Language/framework knowledge
- `PROBLEM_SOLVING`: Algorithm and optimization
- `COMMUNICATION`: Explanation and presentation
- `BEHAVIORAL`: Teamwork, conflict resolution
- `SYSTEM_DESIGN`: Architecture and scalability

### Readiness Categories
- `Strong`: Score 75-100
- `Average`: Score 60-74
- `Needs Improvement`: Score <60

### Hiring Readiness
- `Ready`: Combined score ≥75%
- `Needs Development`: Combined score 55-74%
- `Not Ready`: Combined score <55%

---

## Best Practices

1. **Always check status** after initialization and evaluation
2. **Provide meaningful answers** for better evaluation
3. **Use reasonable time values** (not too quick or slow)
4. **Handle None** when getting current question
5. **Conclude properly** before analyzing final results
6. **Cache results** for analysis and reporting

---

## Performance Considerations

- **Resume Parsing**: O(n) where n = resume length
- **Question Generation**: ~1-2 seconds per question
- **Answer Evaluation**: ~0.5-1 second per answer
- **Interview Completion**: 15-20 minutes for 5 questions

---

## API Rate Limits

Depends on your AI model provider:
- **GitHub Models**: Free tier available
- **Microsoft Foundry**: Check your plan limits
- **OpenAI**: Standard rate limits apply

---

**Last Updated**: February 2026  
**API Version**: 1.0.0
