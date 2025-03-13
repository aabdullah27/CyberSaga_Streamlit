"""
AI Agent module for CyberSaga application.
This module contains the SecurityGuideAgent class that handles scenario generation and user interaction.
"""

import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
import json

# Import prompts
from prompts import (
    SYSTEM_PROMPT,
    SCENARIO_GENERATION_PROMPT,
    DECISION_ANALYSIS_PROMPT,
    LEARNING_MOMENT_PROMPT,
    ASSESSMENT_PROMPT,
    DECISION_POINTS_PROMPT,
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
    
    def generate_scenario(self, security_domain: str, threat_type: str, industry: str = "general", role: str = "general", experience_level: str = "beginner") -> str:
        """
        Generate a cybersecurity scenario based on the user's profile.
        
        Args:
            security_domain: The security domain to focus on (e.g., "phishing", "ransomware")
            threat_type: The specific threat to incorporate
            industry: The industry to focus on (e.g., "healthcare", "finance")
            role: The user's role (e.g., "security analyst", "network administrator")
            experience_level: The user's experience level (e.g., "beginner", "advanced")
        
        Returns:
            A generated cybersecurity scenario as a string
        """
        prompt = SCENARIO_GENERATION_PROMPT.format(
            security_domain=security_domain,
            threat_type=threat_type,
            industry=industry,
            role=role,
            experience_level=experience_level
        )
        
        response = self.agent.run(prompt)
        return response.content
    
    def generate_decision_points(self, scenario_title: str, scenario_domain: str, user_industry: str, user_role: str, experience_level: str) -> List[Dict[str, Any]]:
        """
        Generate decision points for a scenario based on user profile.
        
        Args:
            scenario_title: The title of the scenario
            scenario_domain: The security domain of the scenario
            user_industry: The user's industry
            user_role: The user's role
            experience_level: The user's experience level
        
        Returns:
            A list of decision points as dictionaries
        """
        prompt = DECISION_POINTS_PROMPT.format(
            scenario_title=scenario_title,
            scenario_domain=scenario_domain,
            industry=user_industry,
            role=user_role,
            experience_level=experience_level
        )
        
        try:
            response = self.agent.run(prompt)
            decision_points = json.loads(response.content)
            
            # Validate the structure
            if not isinstance(decision_points, list) or len(decision_points) < 1:
                return None
                
            # Ensure each decision point has the required structure
            for point in decision_points:
                if not all(key in point for key in ["question", "options"]):
                    return None
                if not isinstance(point["options"], list) or len(point["options"]) < 2:
                    return None
                for option in point["options"]:
                    if not all(key in option for key in ["text", "is_correct"]):
                        return None
            
            return decision_points
        except Exception as e:
            print(f"Error generating decision points: {e}")
            return None
    
    def analyze_decision(self, user_decision: str, scenario_description: str, is_correct: Optional[bool] = None) -> str:
        """
        Analyze a user's decision and provide feedback.
        
        Args:
            user_decision: The decision made by the user
            scenario_description: Brief description of the scenario
            is_correct: Whether the user's decision was correct
        
        Returns:
            Analysis of the user's decision
        """
        correctness = "correct" if is_correct else "incorrect"
        prompt = DECISION_ANALYSIS_PROMPT.format(
            user_decision=user_decision,
            scenario_description=scenario_description,
            correctness=correctness
        )
        
        response = self.agent.run(prompt)
        return response.content
    
    def generate_learning_moment(self, scenario_description: str, security_domain: str = "general") -> str:
        """
        Generate a learning moment based on the scenario.
        
        Args:
            scenario_description: Brief description of the scenario
            security_domain: The security domain of the scenario
        
        Returns:
            A learning moment that connects the scenario to practical principles
        """
        prompt = LEARNING_MOMENT_PROMPT.format(
            scenario_description=scenario_description,
            security_domain=security_domain
        )
        
        response = self.agent.run(prompt)
        return response.content
    
    def generate_assessment(self, scenario_title: str, num_questions: int = 3) -> str:
        """
        Generate assessment questions for a completed scenario.
        
        Args:
            scenario_title: Title of the scenario
            num_questions: Number of questions to generate
        
        Returns:
            Assessment questions as a string
        """
        prompt = ASSESSMENT_PROMPT.format(
            scenario_title=scenario_title,
            num_questions=num_questions
        )
        
        response = self.agent.run(prompt)
        return response.content
    
    def generate_recommendations(self, strengths: List[str], knowledge_gaps: List[str], industry: str, role: str) -> str:
        """
        Generate personalized recommendations based on user performance.
        
        Args:
            strengths: List of the user's strengths
            knowledge_gaps: List of the user's knowledge gaps
            industry: The user's industry
            role: The user's role
        
        Returns:
            Personalized recommendations as a string
        """
        prompt = RECOMMENDATION_PROMPT.format(
            strengths=", ".join(strengths),
            knowledge_gaps=", ".join(knowledge_gaps),
            industry=industry,
            role=role
        )
        
        response = self.agent.run(prompt)
        return response.content
