import streamlit as st
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
import os

def generate_certificate(user_name, scenario_title, score, completion_date=None):
    """
    Generate a visually enhanced certificate of completion with larger, clearer text.
    
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
    
    # Create a certificate image (landscape orientation) with higher resolution
    width, height = 1500, 1100  # Increased size for better clarity
    certificate = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(certificate)
    
    # Try to load fonts with larger sizes, fall back to default if not available
    try:
        # For Windows, use Arial or other common fonts with increased sizes
        title_font = ImageFont.truetype("Arial Bold.ttf", 120)
        header_font = ImageFont.truetype("Arial Bold.ttf", 95)
        name_font = ImageFont.truetype("Arial Bold.ttf", 110)
        body_font = ImageFont.truetype("Arial.ttf", 70)
    except IOError:
        # Fall back to default font
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
    
    # Add simple, clean border (avoiding complex patterns that might blur)
    border_color = (0, 120, 60)  # Darker green for better visibility
    draw.rectangle([(40, 40), (width-40, height-40)], outline=border_color, width=10)
    
    # Add header with high contrast colors
    header_color = (0, 100, 50)  # Dark green for better readability
    draw.text((width//2, 150), "CERTIFICATE OF COMPLETION", 
             font=title_font, fill=header_color, anchor="mm")
    
    draw.text((width//2, 250), "CYBERSAGA TRAINING", 
             font=header_font, fill=header_color, anchor="mm")
    
    # Add clean horizontal line
    draw.line([(150, 320), (width-150, 320)], fill=header_color, width=5)
    
    # Add user name with clear, large text
    draw.text((width//2, 420), "This certifies that", 
             font=body_font, fill=(0, 0, 0), anchor="mm")
    
    # Name with high contrast
    draw.text((width//2, 520), user_name, 
             font=name_font, fill=(0, 0, 0), anchor="mm")
    
    # Add scenario details with larger spacing
    draw.text((width//2, 620), "has successfully completed the cybersecurity scenario:", 
             font=body_font, fill=(0, 0, 0), anchor="mm")
    
    # Break long scenario titles into multiple lines if needed
    words = scenario_title.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_line = " ".join(current_line)
        if header_font.getlength(f'"{test_line}"') > width - 300:
            # Remove the last word and complete this line
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]  # Start a new line with the overflow word
    
    # Add any remaining words
    if current_line:
        lines.append(" ".join(current_line))
    
    # Render scenario title (possibly in multiple lines)
    if len(lines) == 1:
        # Single line, render normally
        draw.text((width//2, 720), f'"{scenario_title}"', 
                 font=header_font, fill=header_color, anchor="mm")
    else:
        # Multiple lines, calculate vertical positioning
        start_y = 700
        line_height = 100
        for i, line in enumerate(lines):
            draw.text((width//2, start_y + i * line_height), f'"{line}"' if i == 0 else line + ('"' if i == len(lines)-1 else ""), 
                     font=header_font, fill=header_color, anchor="mm")
    
    # Calculate vertical position based on whether title has multiple lines
    score_y = 820 if len(lines) == 1 else (700 + len(lines) * 100)
    
    # Add score with clear text
    score_text = f"with a score of {score:.0f}%"
    draw.text((width//2, score_y), score_text, 
             font=body_font, fill=(0, 0, 0), anchor="mm")
    
    # Add date with clear formatting
    date_y = score_y + 100
    date_text = f"Date: {completion_date}"
    draw.text((width//2, date_y), date_text, 
             font=body_font, fill=(0, 0, 0), anchor="mm")
    
    # Add CyberSaga signature
    sign_y = date_y + 100
    draw.text((width//2, sign_y), "CyberSaga Training Program", 
             font=body_font, fill=header_color, anchor="mm")
    
    # Convert to high-quality PNG
    buffered = BytesIO()
    certificate.save(buffered, format="PNG", quality=95)  # Higher quality
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
    
    # Display certificate with improved styling for clarity
    st.markdown(
        f"""
        <div style="text-align: center; margin: 20px 0;">
            <img src="data:image/png;base64,{certificate_img}" 
                 style="max-width: 100%; border: 2px solid #ddd;">
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Download button with better styling
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="⬇️ Download Certificate",
            data=base64.b64decode(certificate_img),
            file_name=f"CyberSaga_Certificate_{scenario['title'].replace(' ', '_')}.png",
            mime="image/png",
            use_container_width=True
        )
    
    # Add some space
    st.write("")
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Choose Another Scenario", use_container_width=True):
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
        if st.button("View Progress Dashboard", use_container_width=True):
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