import streamlit as st
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
import os

def generate_certificate(user_name, scenario_title, score, completion_date=None):
    """
    Generate a certificate of completion for a scenario.
    
    Args:
        user_name (str): Name of the user
        scenario_title (str): Title of the completed scenario
        score (float): Score achieved (0-100)
        completion_date (str, optional): Date of completion. Defaults to current date.
    
    Returns:
        str: Base64 encoded certificate image
    """
    # Use current date if not provided
    if completion_date is None:
        completion_date = datetime.now().strftime("%B %d, %Y")
    
    # Create a certificate image (landscape orientation)
    width, height = 1200, 900
    certificate = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(certificate)
    
    # Try to load fonts, fall back to default if not available
    try:
        # For Windows, use Arial or other common fonts
        title_font = ImageFont.truetype("Arial Bold.ttf", 90)  
        header_font = ImageFont.truetype("Arial Bold.ttf", 70)  
        name_font = ImageFont.truetype("Arial Bold.ttf", 80)    
        body_font = ImageFont.truetype("Arial.ttf", 50)         
    except IOError:
        # Fall back to default font
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Add border
    draw.rectangle([(50, 50), (width-50, height-50)], outline=(0, 100, 0), width=5)
    
    # Add header
    draw.text((width//2, 120), "CERTIFICATE OF COMPLETION", font=title_font, fill=(0, 100, 0), anchor="mm")
    draw.text((width//2, 190), "CYBERSAGA TRAINING", font=header_font, fill=(0, 100, 0), anchor="mm")
    
    # Add line
    draw.line([(200, 250), (width-200, 250)], fill=(0, 100, 0), width=3)
    
    # Add user name
    draw.text((width//2, 350), "This certifies that", font=body_font, fill=(0, 0, 0), anchor="mm")
    draw.text((width//2, 420), user_name, font=name_font, fill=(0, 0, 0), anchor="mm")
    
    # Add scenario details
    draw.text((width//2, 500), "has successfully completed the cybersecurity scenario:", font=body_font, fill=(0, 0, 0), anchor="mm")
    draw.text((width//2, 570), f'"{scenario_title}"', font=header_font, fill=(0, 100, 0), anchor="mm")
    
    # Add score
    score_text = f"with a score of {score:.0f}%"
    draw.text((width//2, 640), score_text, font=body_font, fill=(0, 0, 0), anchor="mm")
    
    # Add date
    draw.text((width//2, 720), f"Date: {completion_date}", font=body_font, fill=(0, 0, 0), anchor="mm")
    
    # Add CyberSaga signature
    draw.text((width//2, 780), "CyberSaga Training Program", font=body_font, fill=(0, 0, 0), anchor="mm")
    
    # Convert to base64 for embedding in HTML
    buffered = BytesIO()
    certificate.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

def show_certificate_page():
    """Display the certificate page in the Streamlit app."""
    st.markdown("<h1 class='main-header'>Your Certificate of Completion</h1>", unsafe_allow_html=True)
    
    if "current_scenario" not in st.session_state:
        st.error("No scenario data found. Please complete a scenario first.")
        if st.button("Go to Scenario Selection"):
            st.session_state.current_step = "select_scenario"
            st.rerun()
        return
    
    # Get scenario and user data
    scenario = st.session_state.current_scenario
    scenario_id = scenario["id"]
    user_name = st.session_state.user_profile.profile["personal_info"]["name"]
    
    # Calculate score
    decision_history = st.session_state.scenarios_decision_history.get(scenario_id, [])
    correct_decisions = sum(1 for d in decision_history if d.get("correct", False))
    total_decisions = len(decision_history) or 1
    decision_score = (correct_decisions / total_decisions) * 100
    
    correct_answers = sum(1 for i, q in enumerate(st.session_state.current_assessment["questions"]) 
                         if st.session_state.assessment_answers.get(i, -1) == 
                         next((j for j, opt in enumerate(q["options"]) if opt.get("is_correct", False)), -1))
    total_questions = len(st.session_state.current_assessment["questions"])
    assessment_score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Calculate overall score (weighted average)
    overall_score = (decision_score * 0.6) + (assessment_score * 0.4)
    
    # Generate certificate
    certificate_img = generate_certificate(
        user_name=user_name,
        scenario_title=scenario["title"],
        score=overall_score,
        completion_date=datetime.now().strftime("%B %d, %Y")
    )
    
    # Display certificate
    st.markdown(
        f"""
        <div style="text-align: center; margin: 20px 0;">
            <img src="data:image/png;base64,{certificate_img}" style="max-width: 100%; border: 1px solid #ccc;">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Download button
    st.download_button(
        label="Download Certificate",
        data=base64.b64decode(certificate_img),
        file_name=f"CyberSaga_Certificate_{scenario['title'].replace(' ', '_')}.png",
        mime="image/png"
    )
    
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
            
            # Clear decision history
            st.session_state.decision_history = []
            st.session_state.learning_moments = []
            
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
            
            # Clear decision history
            st.session_state.decision_history = []
            st.session_state.learning_moments = []
            
            # Go to progress dashboard
            st.session_state.current_step = "progress"
            st.rerun()
