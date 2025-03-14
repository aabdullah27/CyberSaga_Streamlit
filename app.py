"""
CyberSaga: An immersive cybersecurity education platform
Main Streamlit application file
"""

import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import certificate_generator

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

if "num_assessment_questions" not in st.session_state:
    st.session_state.num_assessment_questions = 3

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
            email="demo@example.com",
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
    st.markdown("<h1 class='main-header'>Choose Your Cybersecurity Challenge</h1>", unsafe_allow_html=True)
    
    # Display user profile info
    if st.session_state.user_profile:
        user_profile = st.session_state.user_profile.profile
        name = user_profile["personal_info"]["name"]
        email = user_profile["personal_info"].get("email", "")
        industry = user_profile["personal_info"]["industry"]
        role = user_profile["personal_info"]["role"]
        
        # Display user info in a card-like format
        st.markdown(
            f"""
            <div class="user-profile-card">
                <h3>Welcome, {name}!</h3>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Industry:</strong> {industry}</p>
                <p><strong>Role:</strong> {role}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Allow user to select number of assessment questions
    st.markdown("<h3>Assessment Settings</h3>", unsafe_allow_html=True)
    num_questions = st.slider(
        "Number of assessment questions:", 
        min_value=3, 
        max_value=7, 
        value=5, 
        help="Select how many questions you want in your knowledge assessment"
    )
    st.session_state.num_assessment_questions = num_questions
    
    # Display available scenarios
    st.markdown("<h3>Available Scenarios</h3>", unsafe_allow_html=True)
    
    # Get scenarios from session state or initialize
    if "available_scenarios" not in st.session_state:
        st.session_state.available_scenarios = [
            {
                "id": "phishing-1",
                "title": "The Suspicious Email",
                "domain": "phishing",
                "description": "You receive an urgent email asking for sensitive information. Can you identify the phishing attempt and respond appropriately?",
                "difficulty": "beginner",
                "estimated_time": "10-15 minutes"
            },
            {
                "id": "ransomware-1",
                "title": "Locked Out",
                "domain": "ransomware",
                "description": "Your organization is facing a ransomware attack. Navigate the crisis and make critical decisions to minimize damage.",
                "difficulty": "intermediate",
                "estimated_time": "15-20 minutes"
            },
            {
                "id": "social_engineering-1",
                "title": "The Unexpected Visitor",
                "domain": "social_engineering",
                "description": "An unknown person has entered your office claiming to be IT support. Handle the situation while protecting company assets.",
                "difficulty": "beginner",
                "estimated_time": "10-15 minutes"
            },
            {
                "id": "data_protection-1",
                "title": "Data Breach Response",
                "domain": "data_protection",
                "description": "Your company has discovered a potential data breach. Investigate and respond to minimize impact and comply with regulations.",
                "difficulty": "advanced",
                "estimated_time": "20-25 minutes"
            },
            {
                "id": "network_security-1",
                "title": "Unusual Network Activity",
                "domain": "network_security",
                "description": "Security monitoring has detected unusual network traffic patterns. Investigate and respond to the potential threat.",
                "difficulty": "intermediate",
                "estimated_time": "15-20 minutes"
            }
        ]
    
    # Custom CSS for better card styling
    st.markdown("""
    <style>
    .scenario-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .scenario-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    .scenario-domain {
        color: #4CAF50;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .scenario-meta {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
    }
    .difficulty {
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8em;
    }
    .beginner {
        background-color: #4CAF50;
        color: white;
    }
    .intermediate {
        background-color: #FFC107;
        color: black;
    }
    .advanced {
        background-color: #F44336;
        color: white;
    }
    .time {
        color: #9E9E9E;
        font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create rows of 2 scenarios each
    scenarios = st.session_state.available_scenarios
    
    for i in range(0, len(scenarios), 2):
        cols = st.columns(2)
        
        for j in range(2):
            if i + j < len(scenarios):
                scenario = scenarios[i + j]
                
                with cols[j]:
                    st.markdown(
                        f"""
                        <div class="scenario-card">
                            <h4>{scenario["title"]}</h4>
                            <p class="scenario-domain">{scenario["domain"].replace("_", " ").title()}</p>
                            <p>{scenario["description"]}</p>
                            <div class="scenario-meta">
                                <span class="difficulty {scenario["difficulty"]}">{scenario["difficulty"].title()}</span>
                                <span class="time">{scenario["estimated_time"]}</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    if st.button(f"Start Scenario", key=f"start_{scenario['id']}"):
                        st.session_state.current_scenario = scenario
                        st.session_state.current_step = "run_scenario"
                        st.rerun()

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
            
            # Save to scenario
            scenario["narrative"] = narrative
            scenario["current_decision_index"] = 0
            scenario["decision_points"] = []
            st.session_state.current_scenario = scenario
    
    # Display scenario narrative
    st.markdown(f"<div class='scenario-description'>{scenario['narrative']}</div>", unsafe_allow_html=True)
    
    # Get current decision index
    current_index = scenario.get("current_decision_index", 0)
    
    # Generate the current decision point if it doesn't exist yet
    if current_index >= len(scenario.get("decision_points", [])):
        with st.spinner(f"Generating decision point {current_index + 1}..."):
            # Get user profile data for personalization
            user_profile = st.session_state.user_profile.profile
            industry = user_profile["personal_info"]["industry"]
            role = user_profile["personal_info"]["role"]
            experience = user_profile["personal_info"]["experience_level"]
            
            # Generate the next decision point
            decision_point = st.session_state.security_agent.generate_decision_point(
                scenario_title=scenario["title"],
                scenario_domain=scenario["domain"],
                user_industry=industry,
                user_role=role,
                experience_level=experience,
                decision_number=current_index + 1
            )
            
            # If AI generation fails, use fallback decision point
            if not decision_point:
                decision_point = {
                    "question": f"What do you do in this {scenario['domain']} situation?",
                    "options": [
                        {"text": "Take immediate action without verification", "is_correct": False},
                        {"text": "Follow security protocols and report the incident", "is_correct": True},
                        {"text": "Ignore the situation as it's probably not serious", "is_correct": False},
                        {"text": "Ask a colleague what they would do", "is_correct": False}
                    ],
                    "html_content": f"""
                    <h3>Decision Point {current_index + 1}</h3>
                    <p>What do you do in this {scenario['domain']} situation?</p>
                    <ul>
                        <li>Take immediate action without verification</li>
                        <li>Follow security protocols and report the incident</li>
                        <li>Ignore the situation as it's probably not serious</li>
                        <li>Ask a colleague what they would do</li>
                    </ul>
                    <p>Choose your response carefully, as it may impact the security of your organization.</p>
                    """
                }
            
            # Add the decision point to the scenario
            scenario["decision_points"].append(decision_point)
            st.session_state.current_scenario = scenario
    
    # Display current decision point
    decision_point = scenario["decision_points"][current_index]
    
    # Display the HTML content of the decision point
    st.markdown(decision_point["html_content"], unsafe_allow_html=True)
    
    # Display options as buttons
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
                
                # Move to next decision point or summary
                scenario["current_decision_index"] = current_index + 1
                st.session_state.current_scenario = scenario
                
                # If we've reached the maximum number of decision points (3), move to summary
                if scenario["current_decision_index"] >= 3:
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

def show_scenario_summary():
    """Display the scenario summary and knowledge assessment."""
    if "current_scenario" not in st.session_state:
        st.error("No scenario data found. Please start a scenario first.")
        if st.button("Go to Scenario Selection"):
            st.session_state.current_step = "select_scenario"
            st.rerun()
        return
    
    scenario = st.session_state.current_scenario
    scenario_id = scenario["id"]
    
    # Display scenario summary header
    st.markdown(f"<h1 class='main-header'>Scenario Summary: {scenario['title']}</h1>", unsafe_allow_html=True)
    
    # Custom CSS for summary page
    st.markdown("""
    <style>
    .summary-section {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .section-title {
        margin-bottom: 15px;
        color: #4CAF50;
        font-weight: bold;
    }
    .decision-item {
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .decision-question {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .decision-choice {
        margin-bottom: 5px;
    }
    .decision-feedback {
        font-style: italic;
        color: rgba(255, 255, 255, 0.7);
    }
    .correct-choice {
        color: #4CAF50;
    }
    .incorrect-choice {
        color: #F44336;
    }
    .learning-item {
        margin-bottom: 15px;
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 5px;
        border-left: 3px solid #2196F3;
    }
    .assessment-question {
        margin-bottom: 20px;
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 5px;
    }
    .question-text {
        font-weight: bold;
        margin-bottom: 10px;
    }
    .option-item {
        margin: 5px 0;
        padding: 5px;
    }
    .explanation-box {
        margin-top: 10px;
        padding: 10px;
        background-color: rgba(33, 150, 243, 0.1);
        border-radius: 5px;
        border-left: 3px solid #2196F3;
    }
    .completion-message {
        background-color: rgba(76, 175, 80, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 30px;
        border-left: 5px solid #4CAF50;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display completion message
    st.markdown("""
    <div class="completion-message">
        <h2>🎉 Scenario Completed!</h2>
        <p>You've successfully navigated this cybersecurity challenge. Let's review your decisions and test your knowledge.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario overview section
    st.markdown("<div class='summary-section'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>Scenario Overview</h2>", unsafe_allow_html=True)
    
    # Display scenario details
    st.markdown(f"<p><strong>Domain:</strong> {scenario['domain'].replace('_', ' ').title()}</p>", unsafe_allow_html=True)
    st.markdown(f"<p><strong>Difficulty:</strong> {scenario['difficulty'].title()}</p>", unsafe_allow_html=True)
    
    # Display scenario description
    st.markdown(f"<p>{scenario['description']}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Decision history section
    st.markdown("<div class='summary-section'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>Your Decision Journey</h2>", unsafe_allow_html=True)
    
    # Get decision history for current scenario
    decision_history = st.session_state.scenarios_decision_history.get(scenario_id, [])
    
    if not decision_history:
        st.info("No decisions recorded for this scenario.")
    else:
        for i, decision in enumerate(decision_history):
            with st.expander(f"Decision Point {i+1}"):
                decision_text = decision.get("decision", "")
                feedback = decision.get("feedback", "")
                is_correct = decision.get("correct", False)
                
                decision_class = "correct-choice" if is_correct else "incorrect-choice"
                decision_icon = "✓" if is_correct else "✗"
                
                st.markdown(f"""
                <div class='decision-item'>
                    <div class='decision-question'>Your choice: {decision_text}</div>
                    <div class='decision-choice {decision_class}'>{decision_icon} {feedback}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Learning moments section
    st.markdown("<div class='summary-section'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>Key Learning Moments</h2>", unsafe_allow_html=True)
    
    # Get learning moments for current scenario
    learning_moments = st.session_state.scenarios_learning_moments.get(scenario_id, [])
    
    if not learning_moments:
        st.info("No learning moments recorded for this scenario.")
    else:
        for i, moment in enumerate(learning_moments):
            with st.expander(f"Learning Moment {i+1}"):
                st.markdown(f"<div class='learning-item'>{moment}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Knowledge assessment section
    st.markdown("<div class='summary-section'>", unsafe_allow_html=True)
    st.markdown("<h2 class='section-title'>Knowledge Assessment</h2>", unsafe_allow_html=True)
    
    # Generate assessment if not already done
    if "current_assessment" not in st.session_state:
        try:
            num_questions = st.session_state.get("num_assessment_questions", 5)
            
            with st.spinner("Generating your knowledge assessment..."):
                assessment = st.session_state.security_agent.generate_knowledge_assessment(
                    scenario_title=scenario["title"],
                    scenario_domain=scenario["domain"],
                    user_industry=st.session_state.user_profile.profile["personal_info"]["industry"],
                    user_role=st.session_state.user_profile.profile["personal_info"]["role"],
                    experience_level=st.session_state.user_profile.profile["personal_info"]["experience_level"],
                    num_questions=num_questions
                )
                
                st.session_state.current_assessment = assessment
                st.session_state.assessment_answers = {}
                st.session_state.assessment_submitted = False
        except Exception as e:
            st.error(f"Error generating knowledge assessment: {e}")
            st.session_state.current_assessment = {"questions": []}
    
    # Display assessment
    if "current_assessment" in st.session_state and "questions" in st.session_state.current_assessment:
        questions = st.session_state.current_assessment["questions"]
        
        if not questions:
            st.warning("No assessment questions available for this scenario.")
        else:
            if not st.session_state.get("assessment_submitted", False):
                # Display form for answering questions
                with st.form("assessment_form"):
                    for i, question in enumerate(questions):
                        st.markdown(f"<div class='assessment-question'>", unsafe_allow_html=True)
                        st.markdown(f"<p class='question-text'>Question {i+1}: {question['question']}</p>", unsafe_allow_html=True)
                        
                        # Create radio buttons for options
                        options = [opt["text"] for opt in question["options"]]
                        answer = st.radio(
                            f"Select your answer for question {i+1}:",
                            options,
                            key=f"q_{i}",
                            label_visibility="collapsed"
                        )
                        
                        # Store the selected answer
                        if answer:
                            st.session_state.assessment_answers[i] = options.index(answer)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Submit button
                    submitted = st.form_submit_button("Submit Assessment")
                    
                    if submitted:
                        st.session_state.assessment_submitted = True
                        st.rerun()
            else:
                # Display results after submission
                correct_count = 0
                
                for i, question in enumerate(questions):
                    # Get user's answer
                    user_answer_idx = st.session_state.assessment_answers.get(i, -1)
                    
                    # Find correct answer
                    correct_idx = -1
                    for j, opt in enumerate(question["options"]):
                        if opt.get("is_correct", False):
                            correct_idx = j
                            break
                    
                    # Check if user's answer is correct
                    is_correct = user_answer_idx == correct_idx
                    if is_correct:
                        correct_count += 1
                    
                    # Display question and answers
                    with st.expander(f"Question {i+1}"):
                        st.markdown(f"<p class='question-text'>{question['question']}</p>", unsafe_allow_html=True)
                        
                        # Display each option
                        for j, option in enumerate(question["options"]):
                            option_class = ""
                            option_prefix = ""
                            
                            if j == correct_idx:
                                option_class = "correct-choice"
                                option_prefix = "✓ "
                            elif j == user_answer_idx and j != correct_idx:
                                option_class = "incorrect-choice"
                                option_prefix = "✗ "
                            
                            st.markdown(f"<div class='option-item {option_class}'>{option_prefix}{option['text']}</div>", unsafe_allow_html=True)
                        
                        # Display explanation
                        if "explanation" in question:
                            st.markdown(f"<div class='explanation-box'>{question['explanation']}</div>", unsafe_allow_html=True)
                
                # Display overall score
                score_percentage = (correct_count / len(questions)) * 100
                st.markdown(f"<h3>Your Score: {correct_count}/{len(questions)} ({score_percentage:.0f}%)</h3>", unsafe_allow_html=True)
                
                # Record scenario completion
                if not st.session_state.get("scenario_recorded", False):
                    # Calculate points based on correct answers and decisions
                    correct_decisions = sum(1 for d in decision_history if d.get("correct", False))
                    total_decisions = len(decision_history) or 1  # Avoid division by zero
                    decision_score = (correct_decisions / total_decisions) * 100
                    
                    assessment_score = score_percentage
                    
                    # Calculate overall score (weighted average)
                    overall_score = (decision_score * 0.6) + (assessment_score * 0.4)
                    
                    # Prepare performance data
                    performance_data = {
                        "title": scenario.get("title", "Unknown Scenario"),
                        "domain": scenario.get("domain", "general"),
                        "points_earned": int(overall_score),
                        "correct_decisions": correct_decisions,
                        "total_decisions": total_decisions,
                        "assessment_score": score_percentage,
                        "decision_score": decision_score
                    }
                    
                    # Record completion in user profile
                    try:
                        st.session_state.user_profile.record_scenario_completion(scenario["id"], performance_data)
                        
                        # Update skill levels based on domain
                        domain = scenario["domain"]
                        skill_field = f"{domain}_awareness" if domain != "social_engineering" else "social_engineering_defense"
                        
                        # Get current skill levels
                        if "skill_levels" not in st.session_state.user_profile.profile["progress"]:
                            st.session_state.user_profile.profile["progress"]["skill_levels"] = {
                                "phishing_awareness": 0,
                                "ransomware_prevention": 0,
                                "social_engineering_defense": 0,
                                "data_protection": 0,
                                "network_security": 0
                            }
                        
                        skill_levels = st.session_state.user_profile.profile["progress"]["skill_levels"]
                        
                        # Calculate skill improvement (0-5 scale)
                        current_skill = skill_levels.get(skill_field, 0)
                        skill_improvement = (overall_score / 100) * 0.5  # Max 0.5 points per scenario
                        new_skill = min(5, current_skill + skill_improvement)
                        
                        # Update skill level
                        st.session_state.user_profile.profile["progress"]["skill_levels"][skill_field] = new_skill
                        st.session_state.user_profile.save()
                        
                        st.session_state.scenario_recorded = True
                    except Exception as e:
                        st.error(f"Error recording scenario completion: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Certificate button
    if st.session_state.get("assessment_submitted", False):
        if st.button("Generate Completion Certificate"):
            st.session_state.current_step = "certificate"
            st.rerun()
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Choose Another Scenario"):
            # Reset scenario state
            if "current_assessment" in st.session_state:
                del st.session_state.current_assessment
            if "assessment_answers" in st.session_state:
                del st.session_state.assessment_answers
            if "assessment_submitted" in st.session_state:
                del st.session_state.assessment_submitted
            if "scenario_recorded" in st.session_state:
                del st.session_state.scenario_recorded
            
            # Go to scenario selection
            st.session_state.current_step = "select_scenario"
            st.rerun()
    
    with col2:
        if st.button("View Progress Dashboard"):
            # Reset scenario state
            if "current_assessment" in st.session_state:
                del st.session_state.current_assessment
            if "assessment_answers" in st.session_state:
                del st.session_state.assessment_answers
            if "assessment_submitted" in st.session_state:
                del st.session_state.assessment_submitted
            if "scenario_recorded" in st.session_state:
                del st.session_state.scenario_recorded
            
            # Go to progress dashboard
            st.session_state.current_step = "progress"
            st.rerun()

def show_progress_dashboard():
    """Display the user's progress dashboard."""
    st.markdown("<h1 class='main-header'>Your Cybersecurity Progress</h1>", unsafe_allow_html=True)
    
    # Get user profile
    user_profile = st.session_state.user_profile.profile
    
    # Display user info
    st.markdown("<h2>Profile</h2>", unsafe_allow_html=True)
    
    # Profile card with better styling
    st.markdown("""
    <style>
    .profile-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .profile-row {
        display: flex;
        margin-bottom: 10px;
    }
    .profile-label {
        font-weight: bold;
        width: 120px;
    }
    .profile-value {
        flex: 1;
    }
    .skill-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .skill-name {
        font-weight: bold;
        margin-bottom: 10px;
    }
    .skill-bar-container {
        width: 100%;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        margin-bottom: 5px;
    }
    .skill-bar {
        height: 20px;
        border-radius: 5px;
        text-align: center;
        color: white;
        font-weight: bold;
        line-height: 20px;
        font-size: 12px;
    }
    .skill-level-0 {
        background-color: #F44336;
        width: 10%;
    }
    .skill-level-1 {
        background-color: #FF5722;
        width: 20%;
    }
    .skill-level-2 {
        background-color: #FFC107;
        width: 40%;
    }
    .skill-level-3 {
        background-color: #8BC34A;
        width: 60%;
    }
    .skill-level-4 {
        background-color: #4CAF50;
        width: 80%;
    }
    .skill-level-5 {
        background-color: #2E7D32;
        width: 100%;
    }
    .skill-description {
        font-size: 0.9em;
        color: rgba(255, 255, 255, 0.7);
    }
    .scenario-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .scenario-title {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .scenario-meta {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        font-size: 0.9em;
        color: rgba(255, 255, 255, 0.7);
    }
    .scenario-domain {
        background-color: rgba(76, 175, 80, 0.2);
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 0.8em;
    }
    .scenario-points {
        font-weight: bold;
        color: #FFC107;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display profile info
    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-row">
            <div class="profile-label">Name:</div>
            <div class="profile-value">{user_profile['personal_info']['name']}</div>
        </div>
        <div class="profile-row">
            <div class="profile-label">Email:</div>
            <div class="profile-value">{user_profile['personal_info'].get('email', 'Not provided')}</div>
        </div>
        <div class="profile-row">
            <div class="profile-label">Industry:</div>
            <div class="profile-value">{user_profile['personal_info']['industry'].title()}</div>
        </div>
        <div class="profile-row">
            <div class="profile-label">Role:</div>
            <div class="profile-value">{user_profile['personal_info']['role'].title()}</div>
        </div>
        <div class="profile-row">
            <div class="profile-label">Experience:</div>
            <div class="profile-value">{user_profile['personal_info']['experience_level'].title()}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display competency scores
    st.markdown("<h2>Competency Areas</h2>", unsafe_allow_html=True)
    
    # Get skill levels
    skill_levels = user_profile.get("progress", {}).get("skill_levels", {})
    
    # Define main competency areas and their descriptions
    main_competencies = {
        "phishing_awareness": {
            "name": "Phishing Awareness",
            "descriptions": [
                "Novice: Basic understanding of what phishing is",
                "Beginner: Can identify obvious phishing attempts",
                "Intermediate: Recognizes common phishing tactics",
                "Proficient: Can detect sophisticated phishing attempts",
                "Advanced: Expert at identifying and handling all types of phishing",
                "Master: Can train others on phishing prevention"
            ]
        },
        "social_engineering_defense": {
            "name": "Social Engineering Defense",
            "descriptions": [
                "Novice: Basic awareness of social engineering",
                "Beginner: Understands common social engineering tactics",
                "Intermediate: Can identify manipulation attempts",
                "Proficient: Effectively responds to social engineering",
                "Advanced: Skilled at countering various social engineering techniques",
                "Master: Can develop policies to protect against social engineering"
            ]
        },
        "data_protection": {
            "name": "Data Protection",
            "descriptions": [
                "Novice: Basic understanding of data security",
                "Beginner: Follows basic data protection practices",
                "Intermediate: Implements good data security measures",
                "Proficient: Actively protects sensitive data",
                "Advanced: Comprehensive data protection strategies",
                "Master: Expert at data security and compliance"
            ]
        },
        "network_security": {
            "name": "Network Security",
            "descriptions": [
                "Novice: Basic understanding of network security",
                "Beginner: Aware of common network threats",
                "Intermediate: Implements basic network protections",
                "Proficient: Good understanding of network security principles",
                "Advanced: Skilled at securing networks against threats",
                "Master: Expert at network security architecture"
            ]
        }
    }
    
    # Display skill levels
    for skill_id, skill_info in main_competencies.items():
        skill_level = int(skill_levels.get(skill_id, 0))
        skill_name = skill_info["name"]
        
        # Get appropriate description based on level
        description_index = min(skill_level, 5)  # Ensure index is within bounds
        skill_description = skill_info["descriptions"][description_index]
        
        st.markdown(f"""
        <div class="skill-card">
            <div class="skill-name">{skill_name}</div>
            <div class="skill-bar-container">
                <div class="skill-bar skill-level-{skill_level}">Level {skill_level}/5</div>
            </div>
            <div class="skill-description">{skill_description}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display completed scenarios
    st.markdown("<h2>Completed Scenarios</h2>", unsafe_allow_html=True)
    
    # Get completed scenarios
    completed_scenarios = user_profile.get("progress", {}).get("completed_scenarios", [])
    
    if not completed_scenarios:
        st.info("You haven't completed any scenarios yet. Start a scenario to build your skills!")
    else:
        # Sort scenarios by completion date (newest first)
        completed_scenarios.sort(key=lambda x: x.get("completion_date", ""), reverse=True)
        
        for scenario in completed_scenarios:
            # Format domain name for display
            domain = scenario.get("domain", "general").replace("_", " ").title()
            
            # Calculate score percentage
            correct_decisions = scenario.get("correct_decisions", 0)
            total_decisions = scenario.get("total_decisions", 1)
            decision_percentage = (correct_decisions / total_decisions) * 100 if total_decisions > 0 else 0
            
            assessment_score = scenario.get("assessment_score", 0)
            
            # Calculate overall score
            overall_score = int((decision_percentage * 0.6) + (assessment_score * 0.4))
            
            # Format completion date
            completion_date = scenario.get("completion_date", "")
            try:
                # Parse ISO format date and format it nicely
                from datetime import datetime
                date_obj = datetime.fromisoformat(completion_date)
                formatted_date = date_obj.strftime("%B %d, %Y")
            except:
                formatted_date = completion_date
            
            st.markdown(f"""
            <div class="scenario-card">
                <div class="scenario-title">{scenario.get("title", "Unknown Scenario")}</div>
                <div class="scenario-domain">{domain}</div>
                <div class="scenario-meta">
                    <div>Completed: {formatted_date}</div>
                    <div class="scenario-points">Score: {overall_score}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Total points and scenarios completed
    total_points = user_profile.get("progress", {}).get("total_points", 0)
    scenarios_completed = user_profile.get("progress", {}).get("scenarios_completed", 0)
    
    # Display stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Points", total_points)
    
    with col2:
        st.metric("Scenarios Completed", scenarios_completed)
    
    # Navigation button
    if st.button("Choose a New Scenario"):
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
                st.session_state.current_step = "progress"
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
    elif st.session_state.current_step == "progress":
        show_progress_dashboard()
    elif st.session_state.current_step == "certificate":
        certificate_generator.show_certificate_page()
    else:
        st.error("Unknown application state. Returning to welcome screen.")
        st.session_state.current_step = "welcome"
        st.rerun()

if __name__ == "__main__":
    main()