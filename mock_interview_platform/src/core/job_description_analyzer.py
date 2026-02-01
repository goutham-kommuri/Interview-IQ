"""Job description analyzer to extract requirements."""

import re
from typing import List, Set
from src.utils import JobRequirement, CandidateProfile, get_logger

logger = get_logger(__name__)


class JobDescriptionAnalyzer:
    """Analyze job description and extract requirements."""
    
    # Common skill keywords
    SKILL_KEYWORDS = {
        "languages": ["Python", "Java", "JavaScript", "TypeScript", "C++", "C#",
                     "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "SQL"],
        "frameworks": ["React", "Vue", "Angular", "Django", "Flask", "FastAPI",
                      "Spring", "Express", "NextJS", "NestJS", "Rails"],
        "databases": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra",
                     "DynamoDB", "Elasticsearch", "Oracle"],
        "cloud": ["AWS", "Azure", "GCP", "Kubernetes", "Docker", "Lambda"],
        "tools": ["Git", "Docker", "Kubernetes", "Jenkins", "CI/CD", "Terraform"],
        "methodologies": ["Agile", "Scrum", "Kanban", "DevOps", "REST", "GraphQL"],
    }
    
    def __init__(self):
        """Initialize the job description analyzer."""
        self.logger = logger
    
    def analyze(self, jd_text: str, job_title: str = "Tech Role") -> JobRequirement:
        """
        Analyze job description and extract requirements.
        
        Args:
            jd_text: Raw job description text
            job_title: Job title
            
        Returns:
            JobRequirement object with extracted information
        """
        self.logger.info(f"Analyzing job description for: {job_title}")
        
        required_skills = self._extract_required_skills(jd_text)
        preferred_skills = self._extract_preferred_skills(jd_text)
        technologies = self._extract_technologies(jd_text)
        experience_level = self._extract_experience_level(jd_text)
        key_responsibilities = self._extract_responsibilities(jd_text)
        nice_to_have = self._extract_nice_to_have(jd_text)
        role_description = self._extract_role_description(jd_text)
        
        requirement = JobRequirement(
            title=job_title,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            technologies=technologies,
            experience_level=experience_level,
            key_responsibilities=key_responsibilities,
            nice_to_have=nice_to_have,
            role_description=role_description,
        )
        
        self.logger.info(f"Successfully extracted requirements for {job_title}")
        return requirement
    
    def identify_skill_gaps(self, candidate: CandidateProfile,
                           job_requirement: JobRequirement) -> List[str]:
        """
        Identify skill gaps between candidate and job requirements.
        
        Args:
            candidate: Candidate profile
            job_requirement: Job requirements
            
        Returns:
            List of skill gaps
        """
        candidate_skills = set(s.lower() for s in candidate.skills)
        candidate_techs = set(t.lower() for t in candidate.technologies)
        
        required_skills = set(s.lower() for s in job_requirement.required_skills)
        required_techs = set(t.lower() for t in job_requirement.technologies)
        
        # Find missing required skills
        gaps = []
        for skill in required_skills:
            if skill not in candidate_skills:
                gaps.append(f"Required skill: {skill}")
        
        for tech in required_techs:
            if tech not in candidate_techs:
                gaps.append(f"Required technology: {tech}")
        
        return gaps
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills from job description."""
        skills = set()
        text_lower = text.lower()
        
        # Look for "required" section
        required_pattern = r"(?:requirements?|must have)[\s:]*([^\n]+(?:\n(?![A-Z])[^\n]+)*)"
        matches = re.finditer(required_pattern, text, re.IGNORECASE)
        
        requirements_text = text
        for match in matches:
            requirements_text += "\n" + match.group(1)
        
        # Extract skills from requirements
        for skill_category, skill_list in self.SKILL_KEYWORDS.items():
            for skill in skill_list:
                if skill.lower() in requirements_text.lower():
                    skills.add(skill)
        
        return sorted(list(skills))[:10]  # Top 10 skills
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred skills from job description."""
        skills = set()
        text_lower = text.lower()
        
        # Look for "preferred" section
        preferred_pattern = r"(?:preferred|nice to have|bonus)[\s:]*([^\n]+(?:\n(?![A-Z])[^\n]+)*)"
        matches = re.finditer(preferred_pattern, text, re.IGNORECASE)
        
        preferences_text = text
        for match in matches:
            preferences_text += "\n" + match.group(1)
        
        # Extract skills from preferences
        for skill_category, skill_list in self.SKILL_KEYWORDS.items():
            for skill in skill_list:
                if skill.lower() in preferences_text.lower():
                    skills.add(skill)
        
        return sorted(list(skills))[:5]  # Top 5 preferred skills
    
    def _extract_technologies(self, text: str) -> List[str]:
        """Extract technology stack from job description."""
        technologies = set()
        text_lower = text.lower()
        
        # Flatten all technologies
        all_techs = []
        for tech_list in self.SKILL_KEYWORDS.values():
            all_techs.extend(tech_list)
        
        for tech in all_techs:
            if tech.lower() in text_lower:
                technologies.add(tech)
        
        return sorted(list(technologies))[:15]  # Top 15 technologies
    
    def _extract_experience_level(self, text: str) -> str:
        """Extract required experience level."""
        text_lower = text.lower()
        
        if any(phrase in text_lower for phrase in ["entry level", "entry-level", "junior", "0-2 years"]):
            return "entry_level"
        elif any(phrase in text_lower for phrase in ["mid-level", "mid level", "2-5 years", "intermediate"]):
            return "mid_level"
        elif any(phrase in text_lower for phrase in ["senior", "5+ years", "10+ years", "lead", "principal"]):
            return "senior_level"
        else:
            return "mid_level"  # Default
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract key responsibilities from job description."""
        responsibilities = []
        
        # Look for bullet points or numbered lists
        patterns = [
            r"(?:Responsibilities?|Duties?)[\s:]*\n((?:[-•*]\s*.+\n?)+)",
            r"(?:Responsibilities?|Duties?)[\s:]*\n((?:\d+\.\s*.+\n?)+)",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                items = re.findall(r"[-•*\d.]\s*(.+?)(?=[-•*\d.]|$)", match)
                responsibilities.extend([item.strip() for item in items if item.strip()])
        
        # If no structured format found, extract key phrases
        if not responsibilities:
            key_phrases = ["develop", "design", "implement", "manage", "lead",
                          "architect", "maintain", "collaborate", "improve"]
            for line in text.split("\n"):
                if any(phrase in line.lower() for phrase in key_phrases):
                    cleaned = line.strip().lstrip("•-* 0123456789.")
                    if cleaned and len(cleaned) > 10:
                        responsibilities.append(cleaned)
        
        return responsibilities[:8]  # Top 8 responsibilities
    
    def _extract_nice_to_have(self, text: str) -> List[str]:
        """Extract nice-to-have items from job description."""
        nice_to_have = []
        
        # Look for nice-to-have or bonus sections
        pattern = r"(?:Nice to have|Bonus|Plus|Additional)[\s:]*\n((?:[-•*].+\n?)+)"
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        for match in matches:
            items = re.findall(r"[-•*]\s*(.+?)(?=[-•*]|$)", match)
            nice_to_have.extend([item.strip() for item in items if item.strip()])
        
        return nice_to_have[:5]
    
    def _extract_role_description(self, text: str) -> str:
        """Extract overall role description from job description."""
        # Try to get first paragraph or overview
        lines = text.split("\n")
        description_lines = []
        
        for line in lines[:10]:
            stripped = line.strip()
            if stripped and len(stripped) > 20:
                description_lines.append(stripped)
        
        return " ".join(description_lines)[:300]
