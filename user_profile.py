"""
User profile management for CyberSaga application.
This module handles user profiles, progress tracking, and skill assessment.
"""

from typing import Dict, Any
import json
import os
from datetime import datetime


class UserProfile:
    """Class to manage user profile data."""
    
    def __init__(self, user_id: str = "default"):
        """Initialize with default profile structure."""
        self.user_id = user_id
        self.profile = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "personal_info": {
                "name": "",
                "email": "",
                "industry": "",
                "role": "",
                "experience_level": "beginner"
            },
            "progress": {
                "completed_scenarios": [],
                "total_points": 0,
                "scenarios_started": 0,
                "scenarios_completed": 0,
                "skill_levels": {
                    "phishing_awareness": 0,
                    "ransomware_prevention": 0,
                    "social_engineering_defense": 0,
                    "data_protection": 0,
                    "network_security": 0
                }
            },
            "preferences": {
                "difficulty": "adaptive",
                "focus_areas": []
            }
        }
        
        # Load profile if it exists
        self._load_profile()
    
    def _load_profile(self) -> None:
        """Load user profile from storage if it exists."""
        profile_dir = "profiles"
        os.makedirs(profile_dir, exist_ok=True)
        
        profile_path = os.path.join(profile_dir, f"{self.user_id}.json")
        if os.path.exists(profile_path):
            try:
                with open(profile_path, "r") as f:
                    self.profile = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading profile: {e}")
    
    def save(self) -> None:
        """Save user profile to storage."""
        self.profile["last_updated"] = datetime.now().isoformat()
        
        profile_dir = "profiles"
        os.makedirs(profile_dir, exist_ok=True)
        
        profile_path = os.path.join(profile_dir, f"{self.user_id}.json")
        try:
            with open(profile_path, "w") as f:
                json.dump(self.profile, f, indent=2)
        except IOError as e:
            print(f"Error saving profile: {e}")
    
    def update_personal_info(self, name: str, email: str, industry: str, role: str, experience_level: str):
        """Update the user's personal information."""
        self.profile["personal_info"]["name"] = name
        self.profile["personal_info"]["email"] = email
        self.profile["personal_info"]["industry"] = industry
        self.profile["personal_info"]["role"] = role
        self.profile["personal_info"]["experience_level"] = experience_level
        self.save()
    
    def record_scenario_completion(self, scenario_id: str, performance_data: Dict[str, Any]):
        """
        Record the completion of a scenario with performance data.
        
        Args:
            scenario_id: The ID of the completed scenario
            performance_data: Dict containing performance metrics including:
                - points_earned: Points earned in this scenario
                - correct_decisions: List of correct decisions made
                - mistakes: List of incorrect decisions made
        """
        # Extract scenario details from the ID
        scenario_parts = scenario_id.split("-")
        domain = scenario_parts[0] if len(scenario_parts) > 0 else "general"
        
        # Create completion record
        completion = {
            "id": scenario_id,
            "title": performance_data.get("title", "Unknown Scenario"),
            "domain": performance_data.get("domain", "general"),
            "completion_date": datetime.now().isoformat(),
            "points_earned": performance_data.get("points_earned", 0),
            "correct_decisions": performance_data.get("correct_decisions", 0),
            "total_decisions": performance_data.get("total_decisions", 0),
            "assessment_score": performance_data.get("assessment_score", 0)
        }
        
        # Add to completed scenarios list
        self.profile["progress"]["completed_scenarios"].append(completion)
        
        # Update overall progress metrics
        self.profile["progress"]["total_points"] += performance_data.get("points_earned", 0)
        
        # Ensure scenarios_completed exists
        if "scenarios_completed" not in self.profile["progress"]:
            self.profile["progress"]["scenarios_completed"] = 0
            
        self.profile["progress"]["scenarios_completed"] += 1
        
        self.save()
    
    def get_recommended_scenarios(self, available_scenarios: list, count: int = 3) -> list:
        """
        Get recommended scenarios based on user profile and past performance.
        
        Args:
            available_scenarios: List of available scenarios
            count: Number of recommendations to return
            
        Returns:
            List of recommended scenario IDs
        """
        # Get completed scenario IDs
        completed_ids = [s["scenario_id"] for s in self.profile["progress"]["completed_scenarios"]]
        
        # Filter out completed scenarios
        available = [s for s in available_scenarios if s["id"] not in completed_ids]
        
        if not available:
            return []
        
        # Identify weak areas based on mistakes
        mistake_domains = {}
        for completion in self.profile["progress"]["completed_scenarios"]:
            domain = completion.get("domain", "general")
            mistakes = len(completion.get("mistakes", []))
            
            if domain not in mistake_domains:
                mistake_domains[domain] = 0
            
            mistake_domains[domain] += mistakes
        
        # Sort domains by number of mistakes (descending)
        weak_domains = sorted(mistake_domains.items(), key=lambda x: x[1], reverse=True)
        
        # Prioritize scenarios in weak domains
        recommendations = []
        
        # First, add scenarios from weak domains
        for domain, _ in weak_domains:
            domain_scenarios = [s for s in available if s["domain"] == domain]
            recommendations.extend(domain_scenarios)
            
            if len(recommendations) >= count:
                break
        
        # If we still need more recommendations, add other available scenarios
        if len(recommendations) < count:
            remaining = [s for s in available if s not in recommendations]
            recommendations.extend(remaining[:count - len(recommendations)])
        
        return [s["id"] for s in recommendations[:count]]
