"""
AI Agent module for CyberSaga application.
This module contains the SecurityGuideAgent class that handles scenario generation and user interaction.
"""

import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq

# Import prompts
from prompts import (
    SYSTEM_PROMPT,
    SCENARIO_GENERATION_PROMPT,
    DECISION_ANALYSIS_PROMPT,
    LEARNING_MOMENT_PROMPT,
    ASSESSMENT_PROMPT,
    RECOMMENDATION_PROMPT
)

# Load environment variables
load_dotenv()

class SecurityGuideAgent:
    """
    AI Agent that guides users through cybersecurity scenarios.
    This agent generates personalized scenarios, analyzes user decisions,
    provides learning moments, and tracks user progress.
    """
    
    def __init__(self):
        """Initialize the Security Guide Agent with the Groq model."""
        self.agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            description="You are the Security Guide AI Agent for CyberSaga, an immersive cybersecurity education platform.",
            instructions=[SYSTEM_PROMPT],
            markdown=True
        )
        
        # User profile to track progress and personalize content
        self.user_profile = {
            "skill_level": "beginner",
            "industry": "",
            "role": "",
            "completed_scenarios": [],
            "knowledge_gaps": [],
            "strengths": []
        }
    
    def update_user_profile(self, profile_data: Dict[str, Any]) -> None:
        """
        Update the user profile with new information.
        
        Args:
            profile_data: Dictionary containing user profile information
        """
        self.user_profile.update(profile_data)
    
    def generate_scenario(self, security_domain: str, threat_type: str) -> str:
        """
        Generate a cybersecurity scenario based on the user's profile.
        
        Args:
            security_domain: The security domain to focus on (e.g., "phishing", "ransomware")
            threat_type: The specific threat to incorporate
            
        Returns:
            A generated cybersecurity scenario as a string
        """
        prompt = SCENARIO_GENERATION_PROMPT.format(
            role=self.user_profile["role"],
            industry=self.user_profile["industry"],
            skill_level=self.user_profile["skill_level"],
            security_domain=security_domain,
            threat_type=threat_type
        )
        
        response = self.agent.run(prompt)
        return response.content
    
    def analyze_decision(self, user_decision: str, scenario_description: str) -> str:
        """
        Analyze a user's decision in response to a scenario.
        
        Args:
            user_decision: The decision made by the user
            scenario_description: Brief description of the scenario
            
        Returns:
            Analysis of the user's decision
        """
        prompt = DECISION_ANALYSIS_PROMPT.format(
            user_decision=user_decision,
            scenario_description=scenario_description
        )
        
        response = self.agent.run(prompt)
        return response.content
    
    def generate_learning_moment(self, scenario_description: str) -> str:
        """
        Generate a learning moment based on a scenario.
        
        Args:
            scenario_description: Brief description of the scenario
            
        Returns:
            A learning moment that connects the scenario to practical principles
        """
        prompt = LEARNING_MOMENT_PROMPT.format(
            scenario_description=scenario_description
        )
        
        response = self.agent.run(prompt)
        return response.content
    
    def generate_assessment(self, scenario_title: str, num_questions: int = 3) -> str:
        """
        Generate assessment questions for a scenario.
        
        Args:
            scenario_title: Title of the scenario
            num_questions: Number of questions to generate
            
        Returns:
            Assessment questions as a string
        """
        prompt = ASSESSMENT_PROMPT.format(
            num_questions=num_questions,
            scenario_title=scenario_title,
            skill_level=self.user_profile["skill_level"]
        )
        
        response = self.agent.run(prompt)
        return response.content
    
    def recommend_scenarios(self) -> List[Dict[str, str]]:
        """
        Recommend new scenarios based on the user's profile and knowledge gaps.
        
        Returns:
            A list of recommended scenario dictionaries
        """
        # Default to general cybersecurity if no specific gaps identified
        gap_areas = ", ".join(self.user_profile["knowledge_gaps"]) if self.user_profile["knowledge_gaps"] else "general cybersecurity awareness"
        
        prompt = RECOMMENDATION_PROMPT.format(
            gap_areas=gap_areas,
            industry=self.user_profile["industry"]
        )
        
        response = self.agent.run(prompt)
        
        # In a real implementation, we would parse the response into structured data
        # For simplicity, we're returning a placeholder structure
        # This would be enhanced in a production version
        return [
            {
                "title": "Sample Recommendation 1",
                "description": "This is a placeholder for a parsed recommendation",
                "skills": ["skill1", "skill2"],
                "domain": "phishing"
            },
            {
                "title": "Sample Recommendation 2",
                "description": "This is a placeholder for a parsed recommendation",
                "skills": ["skill3", "skill4"],
                "domain": "social engineering"
            },
            {
                "title": "Sample Recommendation 3",
                "description": "This is a placeholder for a parsed recommendation",
                "skills": ["skill5", "skill6"],
                "domain": "data protection"
            }
        ]
