"""Configuration management for the mock interview platform."""

import os
from dotenv import load_dotenv
from typing import Optional


class Config:
    """Configuration class for the mock interview platform."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        load_dotenv()
        
        # Model Configuration
        self.use_foundry = os.getenv("FOUNDRY_API_KEY") is not None
        self.use_gemini = os.getenv("GEMINI_API_KEY") is not None
        self.use_github = os.getenv("GITHUB_TOKEN") is not None
        
        self.foundry_api_key = os.getenv("FOUNDRY_API_KEY")
        self.foundry_endpoint = os.getenv("FOUNDRY_ENDPOINT")
        self.foundry_model_id = os.getenv("FOUNDRY_MODEL_ID", "gpt-4o-mini")
        
        # Gemini Configuration
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-pro")
        
        # GitHub Models Configuration
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_model = os.getenv("GITHUB_MODEL", "openai/gpt-4o-mini")
        
        # Interview Configuration
        self.max_questions = int(os.getenv("MAX_QUESTIONS", 5))
        self.time_per_question = int(os.getenv("TIME_PER_QUESTION", 120))
        self.passing_threshold = int(os.getenv("PASSING_THRESHOLD", 60))
        self.early_termination_threshold = int(
            os.getenv("EARLY_TERMINATION_THRESHOLD", 40)
        )
        
        # Question Generation Configuration
        self.easy_medium_ratio = 0.3
        self.medium_hard_ratio = 0.4
        self.hard_ratio = 0.3
        
    @property
    def model_config(self) -> dict:
        """Get model configuration based on setup."""
        if self.use_gemini:
            return {
                "type": "gemini",
                "api_key": self.gemini_api_key,
                "model": self.gemini_model,
            }
        elif self.use_foundry:
            return {
                "type": "foundry",
                "api_key": self.foundry_api_key,
                "endpoint": self.foundry_endpoint,
                "model_id": self.foundry_model_id,
            }
        else:
            return {
                "type": "github",
                "token": self.github_token,
                "model": self.github_model,
            }
