"""
CyberSaga: An immersive cybersecurity education platform
Main Streamlit application file
"""

import streamlit as st
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import uuid

# Import custom modules
from agent import SecurityGuideAgent
from scenarios import (
    Scenario, DecisionPoint, LearningMoment,
    create_scenario
)
from user_profile import UserProfile

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="CyberSaga - Cybersecurity Adventures",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if "user_profile" not in st.session_state:
    st.session_state.user_profile = UserProfile()

if "security_agent" not in st.session_state:
    st.session_state.security_agent = SecurityGuideAgent()

if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = None

if "current_step" not in st.session_state:
    st.session_state.current_step = "welcome"

if "scenarios_decision_history" not in st.session_state:
    st.session_state.scenarios_decision_history = {}

if "scenarios_learning_moments" not in st.session_state:
    st.session_state.scenarios_learning_moments = {}

# Helper functions
def reset_scenario():
    """Reset the current scenario state."""
    st.session_state.current_scenario = None
    st.session_state.current_step = "select_scenario"

def save_decision(scenario_id, decision, feedback, is_correct):
    """Save a user decision to history for a specific scenario."""
    if scenario_id not in st.session_state.scenarios_decision_history:
        st.session_state.scenarios_decision_history[scenario_id] = []
    
    st.session_state.scenarios_decision_history[scenario_id].append({
        "decision": decision,
        "feedback": feedback,
        "correct": is_correct,
        "summary": f"{'✓' if is_correct else '✗'} Chose to {decision.lower()}",
        "timestamp": datetime.now().isoformat()
    })

def save_learning_moment(scenario_id, learning_moment):
    """Save a learning moment for a specific scenario."""
    if scenario_id not in st.session_state.scenarios_learning_moments:
        st.session_state.scenarios_learning_moments[scenario_id] = []
    
    st.session_state.scenarios_learning_moments[scenario_id].append(learning_moment)

def create_sample_scenarios():
    """Create sample scenarios for demonstration."""
    return [
        {
            "id": "phish-1",
            "title": "The Suspicious Email",
            "description": "You receive an urgent email claiming to be from your company's IT department requesting you to verify your credentials due to a security breach.",
            "domain": "phishing",
            "difficulty": "beginner",
            "industry_context": "corporate"
        },
        {
            "id": "ransomware-1",
            "title": "Locked Out",
            "description": "You arrive at work to find your computer locked with a message demanding payment to restore your files.",
            "domain": "ransomware",
            "difficulty": "intermediate",
            "industry_context": "healthcare"
        },
        {
            "id": "social-1",
            "title": "The Unexpected Visitor",
            "description": "A person you don't recognize is at the office reception claiming to be a new IT contractor who needs access to the server room.",
            "domain": "social_engineering",
            "difficulty": "intermediate",
            "industry_context": "financial"
        },
        {
            "id": "data-1",
            "title": "The Data Transfer Request",
            "description": "A senior executive emails you requesting an urgent transfer of sensitive customer data to an external consultant.",
            "domain": "data_protection",
            "difficulty": "advanced",
            "industry_context": "retail"
        },
        {
            "id": "network-1",
            "title": "The New WiFi Network",
            "description": "While working at a coffee shop, you notice a new WiFi network with your company's name that doesn't require a password.",
            "domain": "network_security",
            "difficulty": "beginner",
            "industry_context": "remote_work"
        }
    ]

# Custom CSS
def load_css():
    """Apply custom styling to the app."""
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #0066cc;
            text-align: center;
            margin-bottom: 1rem;
        }
        .scenario-title {
            font-size: 1.8rem;
            color: #004d99;
            margin-bottom: 1rem;
        }
        .scenario-description {
            font-size: 1.1rem;
            margin-bottom: 2rem;
            background-color: #f0f5ff;
            padding: 1rem;
            border-radius: 5px;
            border-left: 5px solid #0066cc;
            color: #000000;
        }
        .decision-point {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #000000;
        }
        .learning-moment {
            background-color: #e6f7ff;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
            border-left: 5px solid #00cccc;
            color: #000000;
        }
        .feedback-positive {
            color: #00cc66;
            font-weight: bold;
        }
        .feedback-negative {
            color: #ff3300;
            font-weight: bold;
        }
        .progress-section {
            background-color: #f9f9f9;
            padding: 1rem;
            border-radius: 5px;
            margin-top: 2rem;
        }
        .decision-summary {
            font-size: 0.9rem;
            color: #333333;
            background-color: #f5f5f5;
            padding: 0.5rem;
            border-radius: 3px;
            margin-bottom: 0.5rem;
        }
        /* Dark mode compatibility */
        @media (prefers-color-scheme: dark) {
            .scenario-description, .decision-point, .learning-moment, .decision-summary {
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
            }
            .scenario-description {
                background-color: rgba(0, 102, 204, 0.2);
            }
            .learning-moment {
                background-color: rgba(0, 204, 204, 0.2);
            }
            .decision-summary {
                background-color: rgba(255, 255, 255, 0.15);
                color: #ffffff;
            }
        }
        </style>
    """, unsafe_allow_html=True)

load_css()

# Main application components
def show_welcome():
    """Display the welcome page and onboarding."""
    st.markdown("<h1 class='main-header'>Welcome to CyberSaga</h1>", unsafe_allow_html=True)
    
    st.markdown("""
        ### Where Security Education Becomes an Adventure
        
        CyberSaga transforms abstract security concepts into interactive, personalized adventures. 
        Navigate through realistic cybersecurity scenarios where your decisions have meaningful consequences.
        
        Get ready to learn practical security skills through immersive experiences!
    """)
    
    st.image("https://img.freepik.com/free-vector/global-data-security-personal-data-security-cyber-data-security-online-concept-illustration-internet-security-information-privacy-protection_1150-37336.jpg", 
             caption="Embark on your cybersecurity journey")
    
    # Onboarding form
    with st.form("onboarding_form"):
        st.subheader("Tell us about yourself")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name")
            email = st.text_input("Email")
            
        with col2:
            industry_options = [
                "Select your industry",
                "Healthcare",
                "Finance",
                "Education",
                "Technology",
                "Government",
                "Retail",
                "Manufacturing",
                "Other"
            ]
            industry = st.selectbox("Industry", industry_options)
            
            role_options = [
                "Select your role",
                "Executive",
                "Manager",
                "IT Professional",
                "Security Specialist",
                "Administrative",
                "Customer Service",
                "Other"
            ]
            role = st.selectbox("Role", role_options)
        
        experience_options = ["Beginner", "Intermediate", "Advanced"]
        experience = st.select_slider(
            "Cybersecurity Experience Level",
            options=experience_options
        )
        
        submitted = st.form_submit_button("Start My Cybersecurity Journey")
        
        if submitted:
            if name and industry != "Select your industry" and role != "Select your role":
                # Update user profile
                st.session_state.user_profile.update_personal_info(
                    name=name,
                    email=email,
                    industry=industry.lower(),
                    role=role.lower(),
                    experience_level=experience.lower()
                )
                
                # Update agent's user profile
                st.session_state.security_agent.update_user_profile({
                    "skill_level": experience.lower(),
                    "industry": industry.lower(),
                    "role": role.lower()
                })
                
                st.session_state.current_step = "select_scenario"
                st.rerun()
            else:
                st.error("Please fill in all required fields.")
    
    # Skip button for testing
    if st.button("Skip Onboarding (Demo Mode)"):
        st.session_state.user_profile.update_personal_info(
            name="Demo User",
            industry="technology",
            role="it professional",
            experience_level="beginner"
        )
        st.session_state.security_agent.update_user_profile({
            "skill_level": "beginner",
            "industry": "technology",
            "role": "it professional"
        })
        st.session_state.current_step = "select_scenario"
        st.rerun()

def show_scenario_selection():
    """Display the scenario selection page."""
    st.markdown("<h1 class='main-header'>Choose Your Cybersecurity Adventure</h1>", unsafe_allow_html=True)
    
    # Get user profile info
    user_name = st.session_state.user_profile.profile["personal_info"]["name"]
    st.markdown(f"### Hello, {user_name}!")
    st.markdown("Select a scenario to begin your cybersecurity training adventure.")
    
    # Display available scenarios
    scenarios = create_sample_scenarios()
    
    col1, col2 = st.columns(2)
    
    for i, scenario in enumerate(scenarios):
        with col1 if i % 2 == 0 else col2:
            with st.container():
                st.subheader(scenario["title"])
                st.markdown(f"**Difficulty:** {scenario['difficulty'].capitalize()}")
                st.markdown(f"**Domain:** {scenario['domain'].replace('_', ' ').capitalize()}")
                st.markdown(scenario["description"])
                
                if st.button(f"Start: {scenario['title']}", key=f"btn_{scenario['id']}"):
                    st.session_state.current_scenario = scenario
                    st.session_state.current_step = "run_scenario"
                    st.rerun()
    
    # Show user progress in sidebar
    with st.sidebar:
        st.subheader("Your Progress")
        
        # Show skill levels
        st.markdown("#### Skill Levels")
        skill_levels = st.session_state.user_profile.profile["progress"]["skill_levels"]
        
        for skill, level in skill_levels.items():
            skill_name = skill.replace("_", " ").capitalize()
            st.markdown(f"{skill_name}: {level}/10")
            st.progress(level/10)
        
        # Show completed scenarios
        st.markdown("#### Completed Scenarios")
        completed = st.session_state.user_profile.profile["progress"]["completed_scenarios"]
        
        if completed:
            for scenario in completed:
                st.markdown(f"- {scenario['scenario_id']}")
        else:
            st.markdown("No scenarios completed yet.")

def show_scenario():
    """Display the current scenario and handle user interactions."""
    scenario = st.session_state.current_scenario
    
    if not scenario:
        st.error("No scenario selected. Please choose a scenario first.")
        st.session_state.current_step = "select_scenario"
        st.rerun()
        return
    
    st.markdown(f"<h1 class='scenario-title'>{scenario['title']}</h1>", unsafe_allow_html=True)
    
    # First time in this scenario, generate content
    if "narrative" not in scenario:
        with st.spinner("Generating your personalized cybersecurity scenario..."):
            # Get user profile data for personalization
            user_profile = st.session_state.user_profile.profile
            industry = user_profile["personal_info"]["industry"]
            role = user_profile["personal_info"]["role"]
            experience = user_profile["personal_info"]["experience_level"]
            
            # Generate scenario narrative
            narrative = st.session_state.security_agent.generate_scenario(
                security_domain=scenario["domain"],
                threat_type=scenario["domain"],
                industry=industry,
                role=role,
                experience_level=experience
            )
            
            # Generate dynamic decision points based on user profile and scenario
            decision_points = st.session_state.security_agent.generate_decision_points(
                scenario_title=scenario["title"],
                scenario_domain=scenario["domain"],
                user_industry=industry,
                user_role=role,
                experience_level=experience
            )
            
            # If AI generation fails, use fallback decision points
            if not decision_points or len(decision_points) < 2:
                decision_points = [
                    {
                        "question": f"What do you do with the suspicious {scenario['domain']} attempt?",
                        "options": [
                            {"text": "Engage directly with the suspicious content", "is_correct": False},
                            {"text": "Report it to your security team", "is_correct": True},
                            {"text": "Request more information from the sender", "is_correct": False},
                            {"text": "Ignore it without reporting", "is_correct": False}
                        ]
                    },
                    {
                        "question": f"After identifying this as a {scenario['domain']} threat, what's your next step?",
                        "options": [
                            {"text": "Take no further action", "is_correct": False},
                            {"text": "Alert colleagues about the threat", "is_correct": True},
                            {"text": "Change only your primary password", "is_correct": False},
                            {"text": "Test the suspicious content in a sandbox", "is_correct": False}
                        ]
                    },
                    {
                        "question": f"How would you improve your organization's {scenario['domain']} defenses?",
                        "options": [
                            {"text": "No changes needed", "is_correct": False},
                            {"text": "Implement extreme restrictions", "is_correct": False},
                            {"text": "Deploy regular security training", "is_correct": True},
                            {"text": "Limit access to essential personnel only", "is_correct": False}
                        ]
                    }
                ]
            
            # Save to scenario
            scenario["narrative"] = narrative
            scenario["decision_points"] = decision_points
            scenario["current_decision_index"] = 0
            st.session_state.current_scenario = scenario
    
    # Display scenario narrative
    st.markdown(f"<div class='scenario-description'>{scenario['narrative']}</div>", unsafe_allow_html=True)
    
    # Display current decision point
    current_index = scenario.get("current_decision_index", 0)
    
    if current_index < len(scenario["decision_points"]):
        decision_point = scenario["decision_points"][current_index]
        
        st.markdown(f"<div class='decision-point'>{decision_point['question']}</div>", unsafe_allow_html=True)
        
        # Display options
        option_cols = st.columns(len(decision_point["options"]))
        
        for i, option in enumerate(decision_point["options"]):
            with option_cols[i]:
                if st.button(option["text"], key=f"option_{i}"):
                    # Generate feedback based on choice
                    is_correct = option.get("is_correct", False)
                    
                    if is_correct:
                        feedback = st.session_state.security_agent.analyze_decision(
                            user_decision=option["text"],
                            scenario_description=scenario["title"],
                            is_correct=True
                        )
                        save_decision(scenario["id"], option["text"], feedback, True)
                        
                        # Generate learning moment
                        learning_moment = st.session_state.security_agent.generate_learning_moment(
                            scenario_description=scenario["title"],
                            security_domain=scenario["domain"]
                        )
                        save_learning_moment(scenario["id"], learning_moment)
                    else:
                        feedback = st.session_state.security_agent.analyze_decision(
                            user_decision=option["text"],
                            scenario_description=scenario["title"],
                            is_correct=False
                        )
                        save_decision(scenario["id"], option["text"], feedback, False)
                    
                    # Move to next decision point
                    scenario["current_decision_index"] = current_index + 1
                    st.session_state.current_scenario = scenario
                    
                    # If this was the last decision, move to summary
                    if scenario["current_decision_index"] >= len(scenario["decision_points"]):
                        st.session_state.current_step = "scenario_summary"
                    
                    st.rerun()
    
    # Show decision history in sidebar
    with st.sidebar:
        st.subheader("Your Decisions")
        
        # Get decision history for current scenario
        scenario_id = scenario["id"]
        decision_history = st.session_state.scenarios_decision_history.get(scenario_id, [])
        
        if decision_history:
            for i, decision in enumerate(decision_history):
                with st.expander(f"Decision {i+1}"):
                    st.markdown(f"<div class='decision-summary'>{decision.get('summary', 'Made a decision')}</div>", unsafe_allow_html=True)
                    
                    if decision.get("correct", False):
                        st.markdown("<p class='feedback-positive'>✓ Good choice!</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='feedback-negative'>✗ This could be improved</p>", unsafe_allow_html=True)
        else:
            st.info("No decisions made yet.")

def show_scenario_summary():
    """Display the summary of the completed scenario."""
    scenario = st.session_state.current_scenario
    
    if not scenario:
        st.error("No scenario data available.")
        return
    
    st.markdown("<h1 class='main-header'>Scenario Complete!</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='scenario-title'>{scenario['title']} - Summary</h2>", unsafe_allow_html=True)
    
    # Get decision history for current scenario
    scenario_id = scenario["id"]
    decision_history = st.session_state.scenarios_decision_history.get(scenario_id, [])
    learning_moments = st.session_state.scenarios_learning_moments.get(scenario_id, [])
    
    # Calculate performance
    correct_decisions = sum(1 for decision in decision_history if decision.get("correct", False))
    total_decisions = len(decision_history)
    performance_pct = (correct_decisions / total_decisions) * 100 if total_decisions > 0 else 0
    
    # Display performance metrics
    st.markdown("### Your Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Correct Decisions", f"{correct_decisions}/{total_decisions}")
    
    with col2:
        st.metric("Success Rate", f"{performance_pct:.1f}%")
    
    with col3:
        # Determine performance level
        if performance_pct >= 80:
            performance_level = "Expert"
        elif performance_pct >= 60:
            performance_level = "Proficient"
        else:
            performance_level = "Developing"
        
        st.metric("Skill Level", performance_level)
    
    # Display learning moments
    st.markdown("### Key Learning Moments")
    
    for i, moment in enumerate(learning_moments):
        st.markdown(f"<div class='learning-moment'>{moment}</div>", unsafe_allow_html=True)
    
    # Generate assessment questions
    if "assessment_questions" not in scenario:
        with st.spinner("Generating assessment questions..."):
            assessment = st.session_state.security_agent.generate_assessment(
                scenario_title=scenario["title"],
                num_questions=3
            )
            scenario["assessment_questions"] = assessment
            st.session_state.current_scenario = scenario
    
    # Display assessment
    st.markdown("### Knowledge Check")
    st.markdown(scenario["assessment_questions"], unsafe_allow_html=True)
    
    # Record scenario completion in user profile
    if "scenario_recorded" not in scenario:
        # Prepare performance data
        performance_data = {
            "points_earned": int(performance_pct),
            "correct_decisions": [
                {"area": scenario["domain"], "decision": d["decision"]} 
                for d in decision_history if d.get("correct", False)
            ],
            "mistakes": [
                {"area": scenario["domain"], "decision": d["decision"]} 
                for d in decision_history if not d.get("correct", False)
            ],
            "skill_impacts": {
                f"{scenario['domain']}_awareness": 1 if performance_pct >= 70 else 0.5
            }
        }
        
        # Record completion
        st.session_state.user_profile.record_scenario_completion(
            scenario_id=scenario["id"],
            performance_data=performance_data
        )
        
        scenario["scenario_recorded"] = True
        st.session_state.current_scenario = scenario
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Choose Another Scenario"):
            reset_scenario()
            st.rerun()
    
    with col2:
        if st.button("View My Progress Dashboard"):
            st.session_state.current_step = "progress_dashboard"
            st.rerun()

def show_progress_dashboard():
    """Display the user's progress dashboard."""
    st.markdown("<h1 class='main-header'>Your Cybersecurity Progress</h1>", unsafe_allow_html=True)
    
    # Get user profile data
    profile = st.session_state.user_profile.profile
    name = profile["personal_info"]["name"]
    
    st.markdown(f"### {name}'s Security Skills Development")
    
    # Display skill radar chart
    skill_data = profile["progress"]["skill_levels"]
    
    if sum(skill_data.values()) > 0:
        # Convert skill data to format needed for radar chart
        skills = list(skill_data.keys())
        values = list(skill_data.values())
        
        # Display skills as a bar chart (since radar charts are not built into Streamlit)
        st.subheader("Skill Development")
        
        for skill, value in skill_data.items():
            skill_name = skill.replace("_", " ").title()
            st.markdown(f"**{skill_name}**")
            st.progress(value/10)
            st.markdown(f"{value}/10")
    else:
        st.info("Complete scenarios to build your skill profile.")
    
    # Display completed scenarios
    st.subheader("Completed Scenarios")
    
    completed = profile["progress"]["completed_scenarios"]
    
    if completed:
        for i, scenario in enumerate(completed):
            with st.expander(f"Scenario {i+1}: {scenario['scenario_id']}"):
                st.markdown(f"**Completed:** {scenario['completed_at']}")
                st.markdown(f"**Points Earned:** {scenario['performance'].get('points_earned', 0)}")
                
                # Display correct decisions
                correct = scenario['performance'].get('correct_decisions', [])
                if correct:
                    st.markdown("**Correct Decisions:**")
                    for decision in correct:
                        st.markdown(f"- {decision.get('decision', '')}")
                
                # Display mistakes
                mistakes = scenario['performance'].get('mistakes', [])
                if mistakes:
                    st.markdown("**Areas for Improvement:**")
                    for mistake in mistakes:
                        st.markdown(f"- {mistake.get('decision', '')}")
    else:
        st.info("You haven't completed any scenarios yet.")
    
    # Display recommendations
    st.subheader("Recommended Focus Areas")
    
    recommended_areas = profile["assessment"]["recommended_focus_areas"]
    
    if recommended_areas:
        for area in recommended_areas:
            st.markdown(f"- {area.replace('_', ' ').title()}")
    else:
        st.info("Complete more scenarios to receive personalized recommendations.")
    
    # Navigation button
    if st.button("Return to Scenario Selection"):
        st.session_state.current_step = "select_scenario"
        st.rerun()

# Main app logic
def main():
    """Main application function."""
    # Sidebar
    with st.sidebar:
        st.image("https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg", width=100)
        st.title("CyberSaga")
        st.markdown("---")
        
        # Navigation
        if st.session_state.current_step != "welcome":
            if st.button("Home"):
                st.session_state.current_step = "select_scenario"
                st.rerun()
            
            if st.button("My Progress"):
                st.session_state.current_step = "progress_dashboard"
                st.rerun()
            
            if st.button("Start New Scenario"):
                reset_scenario()
                st.rerun()
            
            st.markdown("---")
        
        # About section
        with st.expander("About CyberSaga"):
            st.markdown("""
                CyberSaga transforms abstract security concepts into interactive, 
                personalized adventures. By leveraging AI and an intuitive interface, 
                CyberSaga creates an engaging learning experience that adapts to each 
                user's needs and learning style.
            """)
    
    # Main content based on current step
    if st.session_state.current_step == "welcome":
        show_welcome()
    elif st.session_state.current_step == "select_scenario":
        show_scenario_selection()
    elif st.session_state.current_step == "run_scenario":
        show_scenario()
    elif st.session_state.current_step == "scenario_summary":
        show_scenario_summary()
    elif st.session_state.current_step == "progress_dashboard":
        show_progress_dashboard()
    else:
        st.error("Unknown application state. Returning to welcome screen.")
        st.session_state.current_step = "welcome"
        st.rerun()

if __name__ == "__main__":
    main()