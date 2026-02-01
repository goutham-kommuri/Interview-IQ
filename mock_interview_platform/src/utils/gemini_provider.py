"""Gemini API provider for the mock interview platform."""

import json
import logging
from typing import Optional
import google.generativeai as genai


logger = logging.getLogger(__name__)


class GeminiProvider:
    """Provider for Google Gemini API."""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """Initialize Gemini provider.
        
        Args:
            api_key: Google Gemini API key
            model: Model name (default: gemini-pro)
        """
        self.api_key = api_key
        self.model = model
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)
        
        logger.info(f"Initialized Gemini provider with model: {model}")
    
    def generate_text(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using Gemini API.
        
        Args:
            prompt: Text prompt for generation
            temperature: Temperature for generation (0-2)
            
        Returns:
            Generated text response
        """
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=2048,
                )
            )
            
            if response.text:
                return response.text
            else:
                logger.warning("Empty response from Gemini API")
                return ""
                
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            raise
    
    def generate_json_response(self, prompt: str) -> dict:
        """Generate JSON response using Gemini API.
        
        Args:
            prompt: Prompt asking for JSON response
            
        Returns:
            Parsed JSON response
        """
        try:
            # Add JSON instruction to prompt
            json_prompt = f"{prompt}\n\nReturn ONLY valid JSON, no other text."
            
            response = self.client.generate_content(
                json_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=2048,
                )
            )
            
            if response.text:
                # Try to parse JSON from response
                text = response.text.strip()
                
                # Remove markdown code blocks if present
                if text.startswith("```json"):
                    text = text[7:]
                if text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                
                return json.loads(text.strip())
            else:
                logger.warning("Empty response from Gemini API")
                return {}
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            raise
    
    def evaluate_answer(self, question: str, answer: str, rubric: str) -> dict:
        """Evaluate an answer using Gemini API.
        
        Args:
            question: Interview question
            answer: Candidate answer
            rubric: Evaluation rubric/criteria
            
        Returns:
            Evaluation scores as dictionary
        """
        prompt = f"""You are an expert interview evaluator. Evaluate the following answer.

Question: {question}

Answer: {answer}

Evaluation Rubric:
{rubric}

Provide a JSON response with these exact fields:
{{
    "accuracy_score": <0-100>,
    "clarity_score": <0-100>,
    "depth_score": <0-100>,
    "relevance_score": <0-100>,
    "overall_feedback": "<brief feedback>",
    "strengths": ["<strength1>", "<strength2>"],
    "areas_for_improvement": ["<area1>", "<area2>"]
}}

Only return valid JSON, no additional text."""

        return self.generate_json_response(prompt)
    
    def generate_questions(self, job_role: str, difficulty: str, skill_area: str, count: int = 1) -> list:
        """Generate interview questions using Gemini API.
        
        Args:
            job_role: Target job role
            difficulty: Difficulty level (easy, medium, hard)
            skill_area: Skill area (technical, behavioral, etc.)
            count: Number of questions to generate
            
        Returns:
            List of generated questions
        """
        prompt = f"""Generate {count} interview questions for a {difficulty} {job_role} interview.
Focus on {skill_area} skills.

Provide a JSON response with this exact format:
{{
    "questions": [
        {{
            "text": "<question text>",
            "type": "{skill_area}",
            "difficulty": "{difficulty}"
        }}
    ]
}}

Generate questions that are relevant, specific, and appropriately difficult for a {job_role} position.
Only return valid JSON, no additional text."""

        response = self.generate_json_response(prompt)
        return response.get("questions", [])
    
    def analyze_resume(self, resume_text: str) -> dict:
        """Analyze resume using Gemini API.
        
        Args:
            resume_text: Resume content
            
        Returns:
            Extracted resume information
        """
        prompt = f"""Analyze the following resume and extract key information.

Resume:
{resume_text}

Provide a JSON response with this exact format:
{{
    "name": "<name>",
    "email": "<email>",
    "phone": "<phone>",
    "years_of_experience": <number>,
    "skills": ["<skill1>", "<skill2>", ...],
    "technologies": ["<tech1>", "<tech2>", ...],
    "education": "<education>",
    "experience_summary": "<brief summary>"
}}

Only return valid JSON, no additional text."""

        return self.generate_json_response(prompt)
    
    def analyze_job_description(self, jd_text: str) -> dict:
        """Analyze job description using Gemini API.
        
        Args:
            jd_text: Job description content
            
        Returns:
            Extracted job requirements
        """
        prompt = f"""Analyze the following job description and extract key information.

Job Description:
{jd_text}

Provide a JSON response with this exact format:
{{
    "job_title": "<title>",
    "required_skills": ["<skill1>", "<skill2>", ...],
    "preferred_skills": ["<skill1>", "<skill2>", ...],
    "technologies": ["<tech1>", "<tech2>", ...],
    "experience_level": "<entry/mid/senior>",
    "key_responsibilities": ["<resp1>", "<resp2>", ...]
}}

Only return valid JSON, no additional text."""

        return self.generate_json_response(prompt)
