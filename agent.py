"""
AI Agent module for CyberSaga application.
This module contains the SecurityGuideAgent class that handles scenario generation and user interaction.
"""

from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
import json
import re

# Import prompts
from prompts import (
    SYSTEM_PROMPT,
    SCENARIO_GENERATION_PROMPT,
    DECISION_POINTS_PROMPT,
    DECISION_POINT_PROMPT,
    DECISION_ANALYSIS_PROMPT,
    LEARNING_MOMENT_PROMPT,
    ASSESSMENT_PROMPT,
    RECOMMENDATION_PROMPT,
    KNOWLEDGE_ASSESSMENT_PROMPT
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
            content = response.content.strip()
            
            # Try to find JSON content within the response
            json_match = re.search(r'\[\s*{.*}\s*\]', content, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                decision_points = json.loads(json_str)
            else:
                # If no JSON pattern found, try to parse the entire content
                # Clean up the content to make it valid JSON
                # Remove markdown code block markers if present
                content = re.sub(r'```json|```', '', content)
                content = content.strip()
                decision_points = json.loads(content)
            
            # Validate the structure
            if not isinstance(decision_points, list) or len(decision_points) < 1:
                print("Invalid decision points structure: not a list or empty list")
                return None
                
            # Ensure each decision point has the required structure
            for point in decision_points:
                if not all(key in point for key in ["question", "options"]):
                    print(f"Invalid decision point: missing required keys - {point}")
                    return None
                if not isinstance(point["options"], list) or len(point["options"]) < 2:
                    print(f"Invalid options: not a list or too few options - {point['options']}")
                    return None
                for option in point["options"]:
                    if not all(key in option for key in ["text", "is_correct"]):
                        print(f"Invalid option: missing required keys - {option}")
                        return None
            
            return decision_points
        except Exception as e:
            print(f"Error generating decision points: {e}")
            print(f"Response content: {response.content[:200]}...")
            return None
    
    def generate_decision_point(self, scenario_title: str, scenario_domain: str, 
                               user_industry: str, user_role: str, experience_level: str,
                               decision_number: int) -> Dict[str, Any]:
        """
        Generate a single decision point for a scenario based on user profile.
        
        Args:
            scenario_title: The title of the scenario
            scenario_domain: The security domain of the scenario
            user_industry: The user's industry
            user_role: The user's role
            experience_level: The user's experience level
            decision_number: The number of this decision point in the sequence
        
        Returns:
            A decision point as a dictionary
        """
        prompt = DECISION_POINT_PROMPT.format(
            scenario_title=scenario_title,
            scenario_domain=scenario_domain,
            industry=user_industry,
            role=user_role,
            experience_level=experience_level,
            decision_number=decision_number
        )
        
        try:
            response = self.agent.run(prompt)
            content = response.content.strip()
            
            # Clean up the content to make it valid JSON
            import re
            # Remove markdown code block markers if present
            content = re.sub(r'```json|```', '', content)
            content = content.strip()
            
            # Parse the JSON
            decision_point = json.loads(content)
            
            # Validate the structure
            if not all(key in decision_point for key in ["question", "options", "html_content"]):
                print(f"Invalid decision point: missing required keys - {decision_point}")
                return None
                
            if not isinstance(decision_point["options"], list) or len(decision_point["options"]) < 2:
                print(f"Invalid options: not a list or too few options - {decision_point['options']}")
                return None
                
            for option in decision_point["options"]:
                if not all(key in option for key in ["text", "is_correct"]):
                    print(f"Invalid option: missing required keys - {option}")
                    return None
            
            return decision_point
        except Exception as e:
            print(f"Error generating decision point: {e}")
            print(f"Response content: {response.content[:200]}...")
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
    
    def generate_knowledge_assessment(self, scenario_title: str, scenario_domain: str, user_industry: str, user_role: str, experience_level: str, num_questions: int = 5) -> Dict[str, Any]:
        """
        Generate a knowledge assessment for a completed scenario.
        
        Args:
            scenario_title: Title of the scenario
            scenario_domain: Domain of the scenario (e.g., phishing, ransomware)
            user_industry: User's industry
            user_role: User's role
            experience_level: User's experience level
            num_questions: Number of questions to generate (default: 5)
            
        Returns:
            Dictionary containing assessment questions with options and explanations
        """
        try:
            # Use the assessment generation prompt
            prompt = KNOWLEDGE_ASSESSMENT_PROMPT.format(
                scenario_title=scenario_title,
                scenario_domain=scenario_domain,
                user_industry=user_industry,
                user_role=user_role,
                experience_level=experience_level,
                num_questions=num_questions
            )
            
            # Generate assessment using LLM
            response = self.agent.run(prompt)
            content = response.content.strip()
            
            try:
                # Try to parse the response as JSON
                assessment = json.loads(content)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from the text
                import re
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    assessment = json.loads(json_str)
                else:
                    # If we still can't extract JSON, raise an error
                    raise ValueError("Could not extract valid JSON from response")
            
            # Validate the assessment format
            if "questions" not in assessment or not isinstance(assessment["questions"], list):
                raise ValueError("Invalid assessment format: missing questions list")
            
            if len(assessment["questions"]) < 1:
                raise ValueError("Invalid assessment: no questions generated")
            
            # Ensure each question has the required fields
            for question in assessment["questions"]:
                if "question" not in question:
                    raise ValueError("Invalid question format: missing question text")
                
                if "options" not in question or not isinstance(question["options"], list):
                    raise ValueError("Invalid question format: missing options list")
                
                if len(question["options"]) < 2:
                    raise ValueError("Invalid question format: not enough options")
                
                # Ensure at least one option is marked as correct
                correct_options = [opt for opt in question["options"] if opt.get("is_correct", False)]
                if not correct_options:
                    # If no correct option is marked, mark the first one as correct
                    question["options"][0]["is_correct"] = True
            
            return assessment
        
        except Exception as e:
            print(f"Error generating knowledge assessment: {e}")
            # Return a fallback assessment
            return {
                "questions": [
                    {
                        "question": f"What is the most important first step when dealing with a {scenario_domain} threat?",
                        "options": [
                            {"text": "Immediately shut down all systems", "is_correct": False},
                            {"text": "Report the incident to your security team", "is_correct": True},
                            {"text": "Try to fix the issue yourself", "is_correct": False},
                            {"text": "Ignore it if it doesn't affect your work", "is_correct": False}
                        ],
                        "explanation": f"When facing a {scenario_domain} threat, the first step should always be to report it to your security team who have the expertise to handle it properly."
                    },
                    {
                        "question": f"Which of the following is a best practice for {scenario_domain} prevention?",
                        "options": [
                            {"text": "Only check emails during certain hours", "is_correct": False},
                            {"text": "Share security responsibilities with colleagues", "is_correct": False},
                            {"text": "Regularly update software and security patches", "is_correct": True},
                            {"text": "Use the same password for all accounts", "is_correct": False}
                        ],
                        "explanation": "Regular updates ensure that known vulnerabilities are patched, significantly reducing the risk of security breaches."
                    },
                    {
                        "question": "Why is security awareness training important?",
                        "options": [
                            {"text": "It's only important for IT staff", "is_correct": False},
                            {"text": "It helps all employees recognize and respond to threats", "is_correct": True},
                            {"text": "It's a regulatory requirement but has little practical value", "is_correct": False},
                            {"text": "It only matters for large enterprises", "is_correct": False}
                        ],
                        "explanation": "Security awareness training is crucial for all employees as human error is often the weakest link in security. Well-trained employees can serve as an effective first line of defense."
                    }
                ]
            }
