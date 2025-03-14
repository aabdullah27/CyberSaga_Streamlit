"""
Scenarios module for CyberSaga application.
This module contains classes for different types of cybersecurity scenarios.
"""

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class DecisionPoint:
    """Represents a decision point in a cybersecurity scenario."""
    
    question: str
    options: List[Dict[str, str]]  # List of options with 'text' and 'consequence'
    correct_option_index: int
    explanation: str


@dataclass
class LearningMoment:
    """Represents a learning moment that explains a cybersecurity concept."""
    
    title: str
    content: str
    related_principle: str
    practical_tip: str


class Scenario:
    """Base class for all cybersecurity scenarios."""
    
    def __init__(
        self,
        title: str,
        description: str,
        security_domain: str,
        difficulty: str,
        industry_context: str
    ):
        self.title = title
        self.description = description
        self.security_domain = security_domain
        self.difficulty = difficulty
        self.industry_context = industry_context
        self.decision_points: List[DecisionPoint] = []
        self.learning_moments: List[LearningMoment] = []
        self.completed = False
        
    def add_decision_point(self, decision_point: DecisionPoint) -> None:
        """Add a decision point to the scenario."""
        self.decision_points.append(decision_point)
        
    def add_learning_moment(self, learning_moment: LearningMoment) -> None:
        """Add a learning moment to the scenario."""
        self.learning_moments.append(learning_moment)
        
    def mark_completed(self) -> None:
        """Mark the scenario as completed."""
        self.completed = True


class PhishingScenario(Scenario):
    """Scenario focused on phishing attacks and prevention."""
    
    def __init__(
        self,
        title: str,
        description: str,
        difficulty: str,
        industry_context: str,
        phishing_type: str
    ):
        super().__init__(
            title=title,
            description=description,
            security_domain="phishing",
            difficulty=difficulty,
            industry_context=industry_context
        )
        self.phishing_type = phishing_type


class RansomwareScenario(Scenario):
    """Scenario focused on ransomware attacks and prevention."""
    
    def __init__(
        self,
        title: str,
        description: str,
        difficulty: str,
        industry_context: str,
        ransom_amount: str
    ):
        super().__init__(
            title=title,
            description=description,
            security_domain="ransomware",
            difficulty=difficulty,
            industry_context=industry_context
        )
        self.ransom_amount = ransom_amount


class SocialEngineeringScenario(Scenario):
    """Scenario focused on social engineering attacks and prevention."""
    
    def __init__(
        self,
        title: str,
        description: str,
        difficulty: str,
        industry_context: str,
        attack_vector: str
    ):
        super().__init__(
            title=title,
            description=description,
            security_domain="social_engineering",
            difficulty=difficulty,
            industry_context=industry_context
        )
        self.attack_vector = attack_vector


class DataProtectionScenario(Scenario):
    """Scenario focused on data protection and privacy."""
    
    def __init__(
        self,
        title: str,
        description: str,
        difficulty: str,
        industry_context: str,
        data_type: str
    ):
        super().__init__(
            title=title,
            description=description,
            security_domain="data_protection",
            difficulty=difficulty,
            industry_context=industry_context
        )
        self.data_type = data_type


class NetworkSecurityScenario(Scenario):
    """Scenario focused on network security."""
    
    def __init__(
        self,
        title: str,
        description: str,
        difficulty: str,
        industry_context: str,
        network_type: str
    ):
        super().__init__(
            title=title,
            description=description,
            security_domain="network_security",
            difficulty=difficulty,
            industry_context=industry_context
        )
        self.network_type = network_type


# Factory function to create scenarios based on domain
def create_scenario(domain: str, **kwargs) -> Scenario:
    """
    Factory function to create a scenario of the specified domain.
    
    Args:
        domain: The security domain for the scenario
        **kwargs: Additional arguments for the specific scenario type
        
    Returns:
        A Scenario instance of the appropriate type
    """
    scenario_classes = {
        "phishing": PhishingScenario,
        "ransomware": RansomwareScenario,
        "social_engineering": SocialEngineeringScenario,
        "data_protection": DataProtectionScenario,
        "network_security": NetworkSecurityScenario
    }
    
    if domain not in scenario_classes:
        raise ValueError(f"Unknown scenario domain: {domain}")
    
    return scenario_classes[domain](**kwargs)
