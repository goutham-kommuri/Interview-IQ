"""Main interview flow and orchestration."""

import json
import time
from typing import Dict, List, Any
from src.agents import AIInterviewer
from src.utils import Config, get_logger

logger = get_logger(__name__)


class InterviewOrchestrator:
    """Orchestrates the mock interview process."""
    
    def __init__(self, config: Config = None):
        """Initialize the orchestrator."""
        self.config = config or Config()
        self.interviewer = AIInterviewer(self.config)
        self.logger = logger
    
    def run_interview(self, resume_text: str, jd_text: str,
                     candidate_name: str = "Candidate",
                     job_title: str = "Tech Position",
                     interactive: bool = True) -> Dict[str, Any]:
        """
        Run a complete mock interview session.
        
        Args:
            resume_text: Candidate's resume
            jd_text: Job description
            candidate_name: Candidate's name
            job_title: Job position title
            interactive: Whether to run in interactive mode
            
        Returns:
            Final interview results
        """
        self.logger.info(f"Starting mock interview for {candidate_name}")
        
        # Initialize interview
        init_result = self.interviewer.initialize_interview(
            resume_text, jd_text, candidate_name, job_title
        )
        
        if init_result["status"] != "success":
            self.logger.error(f"Interview initialization failed: {init_result['message']}")
            return init_result
        
        print("\n" + "=" * 80)
        print(f"MOCK INTERVIEW - {candidate_name}")
        print(f"Position: {job_title}")
        print("=" * 80)
        print(f"\nSkill Gaps Identified: {', '.join(init_result.get('skill_gaps', []))}")
        print(f"\nTotal Questions: {init_result['total_questions']}")
        print("\nStarting interview...\n")
        
        # Interview loop
        while True:
            # Get current question
            current_question = self.interviewer.get_current_question()
            if not current_question:
                break
            
            # Display question
            self._display_question(current_question)
            
            # Get answer
            if interactive:
                answer = self._get_interactive_answer()
                time_taken = self._get_time_taken()
            else:
                # For demo purposes, use a sample answer
                answer = self._generate_sample_answer()
                time_taken = 120
            
            # Evaluate answer
            evaluation = self.interviewer.evaluate_answer(answer, time_taken)
            
            # Display evaluation
            self._display_evaluation(evaluation)
            
            # Check if interview continues
            if not evaluation.get("interview_continues", False):
                break
            
            # Display next question prompt
            print("\n" + "-" * 80)
            input("Press Enter to continue to next question...")
            print()
        
        # Generate final report
        print("\n" + "=" * 80)
        print("INTERVIEW CONCLUDED")
        print("=" * 80)
        
        # Generate and display report
        report = self.interviewer.generate_interview_report()
        print(report)
        
        # Return final results
        final_score = self.interviewer.conclude_interview()
        
        return {
            "status": "success",
            "message": "Interview completed",
            "candidate_name": candidate_name,
            "job_title": job_title,
            "final_score": final_score.total_score,
            "readiness": final_score.readiness_category,
            "hiring_ready": final_score.hiring_readiness_indicator,
            "role_fit": final_score.estimated_role_fit,
            "report": report,
        }
    
    def _display_question(self, question: Dict[str, Any]):
        """Display a question to the candidate."""
        print(f"\nQuestion {question['question_number']}/{question['total_questions']}")
        print(f"Difficulty: {question['difficulty'].upper()}")
        print(f"Time Limit: {question['time_limit']} seconds")
        print(f"Type: {question['question_type']}")
        print("-" * 80)
        print(f"\n{question['question_text']}\n")
    
    def _get_interactive_answer(self) -> str:
        """Get answer interactively from user."""
        print("Please provide your answer (press Enter twice when done):")
        lines = []
        empty_count = 0
        
        while empty_count < 1:
            line = input()
            if line:
                lines.append(line)
                empty_count = 0
            else:
                empty_count += 1
        
        return " ".join(lines)
    
    def _get_time_taken(self) -> int:
        """Get time taken for the answer."""
        while True:
            try:
                time_str = input("Time taken (seconds) [default 120]: ")
                if not time_str:
                    return 120
                return int(time_str)
            except ValueError:
                print("Please enter a valid number")
    
    def _generate_sample_answer(self) -> str:
        """Generate a sample answer for demo purposes."""
        return (
            "Based on my understanding, I would approach this problem by first "
            "understanding the requirements and constraints. I would design a solution "
            "that balances performance, scalability, and maintainability. The key is to "
            "use best practices and consider edge cases. For example, I would implement "
            "proper error handling and logging. Additionally, I would write unit tests "
            "to ensure the solution works correctly. Throughout the process, I would "
            "consider monitoring and optimization strategies."
        )
    
    def _display_evaluation(self, evaluation: Dict[str, Any]):
        """Display evaluation results."""
        print("\n" + "=" * 80)
        print("EVALUATION RESULTS")
        print("=" * 80)
        print(f"Overall Score: {evaluation['overall_score']}/100")
        print(f"\nComponent Scores:")
        print(f"  Accuracy: {evaluation['accuracy']}/100")
        print(f"  Clarity: {evaluation['clarity']}/100")
        print(f"  Depth: {evaluation['depth']}/100")
        print(f"  Relevance: {evaluation['relevance']}/100")
        print(f"  Time Efficiency: {evaluation['time_efficiency']}/100")
        
        print(f"\nFeedback:")
        print(evaluation['feedback'])
        
        if evaluation['strengths']:
            print(f"\nStrengths:")
            for strength in evaluation['strengths']:
                print(f"  ✓ {strength}")
        
        if evaluation['areas_for_improvement']:
            print(f"\nAreas for Improvement:")
            for area in evaluation['areas_for_improvement']:
                print(f"  ✗ {area}")


def run_demo():
    """Run a demo interview."""
    # Sample resume
    sample_resume = """
    John Smith
    Email: john.smith@email.com
    Phone: (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 5+ years of experience in building scalable web applications.
    Strong technical foundation with expertise in Python, JavaScript, and cloud technologies.
    
    TECHNICAL SKILLS
    Languages: Python, JavaScript, TypeScript, Java
    Web Frameworks: React, Django, FastAPI, Express
    Databases: PostgreSQL, MongoDB, Redis
    Cloud: AWS, Docker, Kubernetes
    Tools: Git, CI/CD, Jenkins
    
    EXPERIENCE
    Senior Software Engineer - TechCorp (2021-Present)
    - Led development of microservices architecture using Python and FastAPI
    - Implemented CI/CD pipelines with Jenkins and Docker
    - Mentored junior developers on best practices
    
    Software Engineer - StartupXYZ (2018-2021)
    - Built REST APIs using Django and Express
    - Developed React-based frontend applications
    - Implemented automated testing and monitoring
    
    PROJECTS
    Built URL Shortener Service
    Developed Real-time Chat Application
    Created Data Processing Pipeline
    
    EDUCATION
    Bachelor of Science in Computer Science - State University (2018)
    
    CERTIFICATIONS
    AWS Solutions Architect Associate
    """
    
    # Sample job description
    sample_jd = """
    Senior Software Engineer - Backend
    
    Company: InnovateTech
    Location: Remote
    
    ROLE DESCRIPTION
    We are seeking a Senior Software Engineer to join our backend team. You will design and build
    scalable systems serving millions of users. You'll work with cutting-edge technologies and
    mentor junior developers.
    
    REQUIREMENTS
    - 5+ years of software engineering experience
    - Strong proficiency in Python or Java
    - Experience with microservices architecture
    - Experience with cloud platforms (AWS/GCP/Azure)
    - Strong understanding of distributed systems
    - Experience with SQL and NoSQL databases
    - Excellent problem-solving skills
    - Strong communication skills
    
    PREFERRED SKILLS
    - Experience with Kubernetes
    - Knowledge of message queues (Kafka, RabbitMQ)
    - Experience with system design
    - Leadership experience
    - Knowledge of CI/CD best practices
    
    KEY RESPONSIBILITIES
    - Design and implement scalable backend services
    - Architect solutions for high-traffic systems
    - Lead code reviews and knowledge sharing
    - Collaborate with frontend and DevOps teams
    - Optimize system performance and reliability
    - Participate in incident response and post-mortems
    
    NICE TO HAVE
    - Open source contributions
    - Conference speaking experience
    - Experience with gRPC
    - Blockchain knowledge
    """
    
    # Run interview
    config = Config()
    orchestrator = InterviewOrchestrator(config)
    
    results = orchestrator.run_interview(
        sample_resume,
        sample_jd,
        candidate_name="John Smith",
        job_title="Senior Software Engineer - Backend",
        interactive=False  # Set to True for interactive mode
    )
    
    print("\n" + "=" * 80)
    print("INTERVIEW SUMMARY")
    print("=" * 80)
    print(f"Candidate: {results['candidate_name']}")
    print(f"Position: {results['job_title']}")
    print(f"Final Score: {results['final_score']}/100")
    print(f"Readiness: {results['readiness']}")
    print(f"Hiring Ready: {results['hiring_ready']}")
    print(f"Role Fit: {results['role_fit']}%")


if __name__ == "__main__":
    run_demo()
