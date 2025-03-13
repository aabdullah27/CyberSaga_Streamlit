"""
User profile management for CyberSaga application.
This module handles user profiles, progress tracking, and skill assessment.
"""

from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime


class UserProfile:
    """
    Manages user profiles and progress tracking for CyberSaga.
    """
    
    def __init__(self, user_id: str = "default"):
        """
        Initialize a user profile.
        
        Args:
            user_id: Unique identifier for the user
        """
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
                "experience_level": "beginner"  # beginner, intermediate, advanced
            },
            "progress": {
                "completed_scenarios": [],
                "current_scenario": None,
                "skill_levels": {
                    "phishing_awareness": 0,
                    "ransomware_prevention": 0,
                    "social_engineering_defense": 0,
                    "data_protection": 0,
                    "network_security": 0,
                    "incident_response": 0,
                    "password_management": 0,
                    "secure_communication": 0
                },
                "achievements": [],
                "total_points": 0
            },
            "preferences": {
                "learning_style": "narrative",  # narrative, technical, practical
                "difficulty": "adaptive",  # easy, moderate, challenging, adaptive
                "session_duration": 15  # minutes
            },
            "assessment": {
                "knowledge_gaps": [],
                "strengths": [],
                "recommended_focus_areas": []
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
    
    def update_personal_info(self, **kwargs) -> None:
        """
        Update personal information in the user profile.
        
        Args:
            **kwargs: Key-value pairs of personal information to update
        """
        for key, value in kwargs.items():
            if key in self.profile["personal_info"]:
                self.profile["personal_info"][key] = value
        self.save()
    
    def update_preferences(self, **kwargs) -> None:
        """
        Update user preferences.
        
        Args:
            **kwargs: Key-value pairs of preferences to update
        """
        for key, value in kwargs.items():
            if key in self.profile["preferences"]:
                self.profile["preferences"][key] = value
        self.save()
    
    def record_scenario_completion(self, scenario_id: str, performance_data: Dict[str, Any]) -> None:
        """
        Record the completion of a scenario and update skills accordingly.
        
        Args:
            scenario_id: ID of the completed scenario
            performance_data: Data about user performance in the scenario
        """
        # Add to completed scenarios
        completion_record = {
            "scenario_id": scenario_id,
            "completed_at": datetime.now().isoformat(),
            "performance": performance_data
        }
        
        self.profile["progress"]["completed_scenarios"].append(completion_record)
        self.profile["progress"]["current_scenario"] = None
        
        # Update skill levels based on performance
        if "skill_impacts" in performance_data:
            for skill, impact in performance_data["skill_impacts"].items():
                if skill in self.profile["progress"]["skill_levels"]:
                    current_level = self.profile["progress"]["skill_levels"][skill]
                    self.profile["progress"]["skill_levels"][skill] = max(0, min(10, current_level + impact))
        
        # Update total points
        if "points_earned" in performance_data:
            self.profile["progress"]["total_points"] += performance_data["points_earned"]
        
        # Update assessment based on performance
        self._update_assessment(performance_data)
        
        self.save()
    
    def set_current_scenario(self, scenario_id: str) -> None:
        """
        Set the current active scenario for the user.
        
        Args:
            scenario_id: ID of the current scenario
        """
        self.profile["progress"]["current_scenario"] = scenario_id
        self.save()
    
    def _update_assessment(self, performance_data: Dict[str, Any]) -> None:
        """
        Update the user's knowledge assessment based on scenario performance.
        
        Args:
            performance_data: Data about user performance in a scenario
        """
        # Update knowledge gaps
        if "mistakes" in performance_data and performance_data["mistakes"]:
            for mistake in performance_data["mistakes"]:
                if mistake["area"] not in self.profile["assessment"]["knowledge_gaps"]:
                    self.profile["assessment"]["knowledge_gaps"].append(mistake["area"])
        
        # Update strengths
        if "correct_decisions" in performance_data and performance_data["correct_decisions"]:
            for decision in performance_data["correct_decisions"]:
                if decision["area"] not in self.profile["assessment"]["strengths"]:
                    self.profile["assessment"]["strengths"].append(decision["area"])
        
        # Update recommended focus areas based on gaps and strengths
        self._calculate_recommended_focus_areas()
    
    def _calculate_recommended_focus_areas(self) -> None:
        """Calculate recommended focus areas based on current assessment."""
        # Simple algorithm: prioritize areas with gaps that aren't strengths
        focus_areas = []
        
        for gap in self.profile["assessment"]["knowledge_gaps"]:
            if gap not in self.profile["assessment"]["strengths"]:
                focus_areas.append(gap)
        
        # Limit to top 3 focus areas
        self.profile["assessment"]["recommended_focus_areas"] = focus_areas[:3]
    
    def get_skill_level(self, skill: str) -> int:
        """
        Get the user's level in a specific skill.
        
        Args:
            skill: The skill to check
            
        Returns:
            Skill level from 0-10
        """
        return self.profile["progress"]["skill_levels"].get(skill, 0)
    
    def get_overall_skill_level(self) -> str:
        """
        Get the user's overall skill level category.
        
        Returns:
            Skill level category (beginner, intermediate, advanced)
        """
        # Calculate average skill level
        skill_values = self.profile["progress"]["skill_levels"].values()
        if not skill_values:
            return "beginner"
        
        avg_skill = sum(skill_values) / len(skill_values)
        
        if avg_skill < 3:
            return "beginner"
        elif avg_skill < 7:
            return "intermediate"
        else:
            return "advanced"
    
    def get_recommended_scenarios(self) -> List[str]:
        """
        Get recommended scenario types based on user assessment.
        
        Returns:
            List of recommended scenario types
        """
        return self.profile["assessment"]["recommended_focus_areas"]
