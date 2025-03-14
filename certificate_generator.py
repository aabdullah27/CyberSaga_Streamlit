import streamlit as st
import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime

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
    width, height = 2000, 1400  # Further increased size for better visibility
    certificate = Image.new('RGB', (width, height), color=(252, 252, 252))
    draw = ImageDraw.Draw(certificate)
    
    # Try to load fonts with properly sized fonts, fall back to default if not available
    try:
        # For Windows, use Arial or other common fonts with increased sizes
        title_font = ImageFont.truetype("Arial Bold.ttf", 280)  # Was 160
        header_font = ImageFont.truetype("Arial Bold.ttf", 220)  # Was 130
        name_font = ImageFont.truetype("Arial Bold.ttf", 280)  # Was 160
        body_font = ImageFont.truetype("Arial.ttf", 160)  # Was 95
    except IOError:
        try:
            # Try system font locations for Linux/macOS
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 160)
            header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 130)
            name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 160)
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 95)
        except IOError:
            # Final fallback to default
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
    
    # Add decorative border
    border_width = 25
    outer_border_color = (0, 100, 50)  # Dark green for main border
    inner_border_color = (20, 140, 70)  # Slightly lighter green for inner accent
    
    # Outer border (thicker)
    draw.rectangle([(0, 0), (width, height)], outline=outer_border_color, width=border_width)
    
    # Inner border (thinner)
    draw.rectangle([(60, 60), (width-60, height-60)], outline=inner_border_color, width=10)
    
    # Add header with high contrast colors
    header_color = (0, 120, 60)  # Rich green for better readability
    accent_color = (0, 150, 75)  # Slightly lighter green for accents
    
    # Certificate title
    draw.text((width//2, 180), "CERTIFICATE OF COMPLETION", 
             font=title_font, fill=header_color, anchor="mm")
    
    # Program name
    draw.text((width//2, 320), "CYBERSAGA TRAINING", 
             font=header_font, fill=header_color, anchor="mm")
    
    # Add decorative horizontal line with gradient effect
    line_y = 420
    line_width = 8
    for i in range(width-300):
        # Create a gradient effect on the line
        x = 150 + i
        if i < width//4:
            line_color = (0, 100, 50)
        elif i < width//2:
            line_color = (0, 120, 60)
        elif i < 3*width//4:
            line_color = (0, 120, 60)
        else:
            line_color = (0, 100, 50)
        draw.line([(x, line_y), (x, line_y+line_width)], fill=line_color, width=1)
    
    # Add user name with clear, large text
    draw.text((width//2, 550), "This certifies that", 
             font=body_font, fill=(40, 40, 40), anchor="mm")
    
    # Name with high prominence
    name_y = 680
    draw.text((width//2, name_y), user_name, 
             font=name_font, fill=(0, 0, 0), anchor="mm")
    
    # Add subtle underline for name
    name_width = name_font.getlength(user_name)
    draw.line([(width//2 - name_width//2 - 50, name_y + 80), 
               (width//2 + name_width//2 + 50, name_y + 80)], 
              fill=accent_color, width=3)
    
    # Add scenario details with larger spacing
    draw.text((width//2, 830), "has successfully completed the cybersecurity scenario:", 
             font=body_font, fill=(40, 40, 40), anchor="mm")
    
    # Break long scenario titles into multiple lines if needed
    words = scenario_title.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_line = " ".join(current_line)
        if header_font.getlength(f'"{test_line}"') > width - 400:
            # Remove the last word and complete this line
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]  # Start a new line with the overflow word
    
    # Add any remaining words
    if current_line:
        lines.append(" ".join(current_line))
    
    # Render scenario title (possibly in multiple lines)
    if len(lines) == 1:
        # Single line, render normally with decorative quotes
        scenario_y = 950
        draw.text((width//2, scenario_y), f'"{scenario_title}"', 
                 font=header_font, fill=header_color, anchor="mm")
    else:
        # Multiple lines, calculate vertical positioning
        scenario_y = 920
        line_height = 130
        for i, line in enumerate(lines):
            draw.text((width//2, scenario_y + i * line_height), 
                     f'"{line}"' if i == 0 else line + ('"' if i == len(lines)-1 else ""), 
                     font=header_font, fill=header_color, anchor="mm")
    
    # Calculate vertical position based on whether title has multiple lines
    score_y = 1080 if len(lines) == 1 else (920 + len(lines) * 130 + 50)
    
    # Add score with highlight
    score_text = f"with a score of {score:.0f}%"
    draw.text((width//2, score_y), score_text, 
             font=body_font, fill=(0, 0, 0), anchor="mm")
    
    # Add date with clear formatting and decoration
    date_y = score_y + 130
    date_text = f"Date: {completion_date}"
    
    # Create a subtle background for the date
    date_width = body_font.getlength(date_text)
    date_height = 100
    draw.rectangle([
        (width//2 - date_width//2 - 30, date_y - date_height//2 + 10),
        (width//2 + date_width//2 + 30, date_y + date_height//2 - 10)
    ], fill=(245, 250, 245), outline=accent_color, width=2)
    
    draw.text((width//2, date_y), date_text, 
             font=body_font, fill=(0, 0, 0), anchor="mm")
    
    # Add CyberSaga signature with visual emphasis
    sign_y = date_y + 130
    sig_text = "CyberSaga Training Program"
    draw.text((width//2, sign_y), sig_text, 
             font=body_font, fill=header_color, anchor="mm")
    
    # Add decorative element below signature
    sig_width = body_font.getlength(sig_text)
    draw.line([(width//2 - sig_width//2, sign_y + 50), 
               (width//2 + sig_width//2, sign_y + 50)], 
              fill=accent_color, width=3)
    
    # Convert to high-quality PNG
    buffered = BytesIO()
    certificate.save(buffered, format="PNG", quality=100)  # Maximum quality
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
                 style="max-width: 100%; border: 2px solid #ddd; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
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
