"""Resume analyzer to extract candidate information."""

import re
from typing import List, Dict, Optional
from src.utils import CandidateProfile, get_logger

logger = get_logger(__name__)


class ResumeAnalyzer:
    """Analyze resume and extract candidate profile."""
    
    # Common technical skills and technologies
    TECH_SKILLS = {
        "languages": ["Python", "Java", "JavaScript", "TypeScript", "C++", "C#", 
                     "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin"],
        "web_frameworks": ["React", "Vue", "Angular", "Django", "Flask", "FastAPI",
                          "Spring", "Express", "NextJS", "NestJS"],
        "databases": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra",
                     "DynamoDB", "Elasticsearch"],
        "cloud": ["AWS", "Azure", "GCP", "Kubernetes", "Docker"],
        "tools": ["Git", "Docker", "Kubernetes", "Jenkins", "CI/CD"],
    }
    
    SOFT_SKILLS = ["Communication", "Leadership", "Problem Solving", "Teamwork",
                   "Time Management", "Adaptability", "Critical Thinking"]
    
    def __init__(self):
        """Initialize the resume analyzer."""
        self.logger = logger
    
    def analyze(self, resume_text: str, candidate_name: str = "Unknown") -> CandidateProfile:
        """
        Analyze resume and extract candidate profile.
        
        Args:
            resume_text: Raw resume text
            candidate_name: Candidate's name
            
        Returns:
            CandidateProfile object with extracted information
        """
        self.logger.info(f"Analyzing resume for candidate: {candidate_name}")
        
        # Extract information
        skills = self._extract_skills(resume_text)
        technologies = self._extract_technologies(resume_text)
        projects = self._extract_projects(resume_text)
        education = self._extract_education(resume_text)
        certifications = self._extract_certifications(resume_text)
        years_of_exp = self._extract_experience_years(resume_text)
        contact_info = self._extract_contact_info(resume_text)
        summary = self._extract_summary(resume_text)
        strengths = self._identify_strengths(skills, technologies, projects)
        
        profile = CandidateProfile(
            name=candidate_name,
            email=contact_info.get("email", ""),
            phone=contact_info.get("phone", ""),
            years_of_experience=years_of_exp,
            skills=skills,
            technologies=technologies,
            projects=projects,
            education=education,
            certifications=certifications,
            summary=summary,
            strengths=strengths,
        )
        
        self.logger.info(f"Successfully extracted profile for {candidate_name}")
        return profile
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical and soft skills from resume."""
        skills = set()
        text_lower = text.lower()
        
        # Extract technical skills
        for skill_category, skill_list in self.TECH_SKILLS.items():
            for skill in skill_list:
                if skill.lower() in text_lower:
                    skills.add(skill)
        
        # Extract soft skills
        for skill in self.SOFT_SKILLS:
            if skill.lower() in text_lower:
                skills.add(skill)
        
        return sorted(list(skills))
    
    def _extract_technologies(self, text: str) -> List[str]:
        """Extract technology stack from resume."""
        technologies = set()
        text_lower = text.lower()
        
        # Flatten all tech skills
        all_techs = []
        for skill_list in self.TECH_SKILLS.values():
            all_techs.extend(skill_list)
        
        for tech in all_techs:
            if tech.lower() in text_lower:
                technologies.add(tech)
        
        return sorted(list(technologies))
    
    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract project information from resume."""
        projects = []
        
        # Simple project extraction - look for patterns
        project_pattern = r"(?:project|built|developed|created):\s*([^\n]+)"
        matches = re.finditer(project_pattern, text, re.IGNORECASE)
        
        for match in matches:
            project_name = match.group(1).strip()
            projects.append({
                "name": project_name,
                "description": project_name,
            })
        
        return projects
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information from resume."""
        education = []
        
        # Look for degree patterns
        degree_pattern = r"(?:B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|Ph\.?D\.?)\s+(?:in\s+)?([^\n]+)"
        matches = re.finditer(degree_pattern, text)
        
        for match in matches:
            degree = match.group(0).strip()
            field = match.group(1).strip()
            education.append({
                "degree": degree,
                "field": field,
            })
        
        return education
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications from resume."""
        certifications = []
        
        # Look for common certifications
        cert_keywords = ["certified", "certification", "credential", "AWS", "GCP", 
                        "Azure", "Kubernetes", "Scrum", "PMP"]
        
        for line in text.split("\n"):
            if any(keyword.lower() in line.lower() for keyword in cert_keywords):
                certifications.append(line.strip())
        
        return certifications[:5]  # Limit to 5
    
    def _extract_experience_years(self, text: str) -> int:
        """Extract years of experience from resume."""
        # Look for experience patterns
        exp_pattern = r"(?:(\d+)\s*(?:\+)?\s*years?)"
        matches = re.findall(exp_pattern, text, re.IGNORECASE)
        
        if matches:
            years = [int(m) for m in matches]
            return max(years)
        
        # Default to 0 if not found
        return 0
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from resume."""
        info = {}
        
        # Email pattern
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        email_match = re.search(email_pattern, text)
        if email_match:
            info["email"] = email_match.group(0)
        
        # Phone pattern
        phone_pattern = r"(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})"
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            info["phone"] = phone_match.group(0)
        
        return info
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary from resume."""
        # Look for summary or objective sections
        summary_pattern = r"(?:PROFESSIONAL\s+SUMMARY|OBJECTIVE|ABOUT)[\s:]*([^\n]{0,200})"
        match = re.search(summary_pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        # If no summary found, use first few lines
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return " ".join(lines[:3])
    
    def _identify_strengths(self, skills: List[str], 
                           technologies: List[str],
                           projects: List[Dict[str, str]]) -> List[str]:
        """Identify candidate strengths based on extracted info."""
        strengths = []
        
        if len(technologies) >= 5:
            strengths.append("Strong technical foundation with diverse tech stack")
        
        if len(projects) >= 3:
            strengths.append("Proven project delivery experience")
        
        if any(skill in ["Leadership", "Communication"] for skill in skills):
            strengths.append("Strong soft skills and communication")
        
        if any(tech in ["AWS", "Azure", "GCP", "Kubernetes"] for tech in technologies):
            strengths.append("Cloud infrastructure expertise")
        
        return strengths
