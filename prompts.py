"""
Prompts for the CyberSaga Streamlit application.
These prompts are used to guide the AI agent in generating personalized cybersecurity scenarios.
"""

# System prompt for the AI agent
SYSTEM_PROMPT = """
You are the Security Guide AI Agent for CyberSaga, an immersive cybersecurity education platform.
Your role is to create engaging, educational cybersecurity scenarios that adapt to the user's industry, 
role, and skill level. Each scenario should be realistic, relevant to current threats, and provide 
valuable learning opportunities.

Maintain narrative coherence while tracking learning objectives. Analyze user decisions to identify 
knowledge gaps and provide contextual explanations when users make security mistakes.
"""

# Prompt for generating a new cybersecurity scenario
SCENARIO_GENERATION_PROMPT = """
Create an immersive cybersecurity scenario for a user who works as {role} in the {industry} industry 
with a {skill_level} level of cybersecurity knowledge.

The scenario should:
1. Be realistic and relevant to the user's industry
2. Focus on the {security_domain} domain
3. Present a narrative with clear decision points
4. Include realistic consequences for different choices
5. Incorporate current threat intelligence about {threat_type}
6. Be engaging and educational

Begin the scenario with a brief introduction to set the context, then present the initial situation 
that requires the user to make a security decision.
"""

# Prompt for analyzing user decisions
DECISION_ANALYSIS_PROMPT = """
Analyze the user's decision to {user_decision} in response to the {scenario_description} scenario.

Consider:
1. Whether this decision follows cybersecurity best practices
2. Potential immediate and long-term consequences
3. Alternative approaches that might be more secure
4. The specific security principles relevant to this situation

Provide feedback that is educational but not judgmental, and suggest how the user might improve 
their security decision-making in similar situations.
"""

# Prompt for generating learning moments
LEARNING_MOMENT_PROMPT = """
Create a brief "learning moment" that connects the user's experience in the {scenario_description} 
scenario to practical cybersecurity principles.

The learning moment should:
1. Highlight the key security concept(s) demonstrated in this scenario
2. Explain why certain practices are more secure than others
3. Provide a real-world example of how this security principle has been relevant
4. Offer a practical tip the user can apply in their daily digital interactions

Keep the explanation concise, engaging, and directly relevant to the user's industry and role.
"""

# Prompt for assessment questions
ASSESSMENT_PROMPT = """
Generate {num_questions} multiple-choice assessment questions to evaluate the user's understanding 
of the cybersecurity concepts covered in the {scenario_title} scenario.

Each question should:
1. Test comprehension of a specific security principle
2. Have 4 possible answers with only one correct option
3. Include a brief explanation of why the correct answer is right
4. Be relevant to the user's industry context

Vary the difficulty based on the user's current skill level of {skill_level}.
"""

# Prompt for generating next scenario recommendations
RECOMMENDATION_PROMPT = """
Based on the user's performance in previous scenarios and identified knowledge gaps in {gap_areas},
recommend 3 new cybersecurity scenarios that would help strengthen their understanding.

For each recommendation:
1. Provide a compelling title
2. Include a brief description of the scenario
3. Explain which specific security skills it would help develop
4. Connect it to the user's industry context of {industry}

Prioritize scenarios that address the user's most significant knowledge gaps while maintaining
an engaging progression of difficulty.
"""
