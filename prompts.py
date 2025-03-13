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
Create an engaging cybersecurity scenario focused on {security_domain} threats, specifically {threat_type}.
The scenario should be tailored for someone in the {industry} industry with a {role} role and {experience_level} experience level.

Your scenario should:
1. Begin with a realistic situation that the user might encounter
2. Include specific details that make it relevant to their industry and role
3. Present a cybersecurity challenge that requires decision-making
4. Be educational while remaining engaging
5. Be written in second person ("you")
6. Be approximately 150-200 words

Format the scenario as HTML with appropriate paragraph breaks for readability. Include the following sections ONLY:
- A heading with the threat type (e.g., "Phishing Threat Scenario")
- A brief introduction to the type of threat (bullet points of common attack vectors)
- An "Initial Situation" heading followed by the scenario description

DO NOT include any decision points or questions - these will be generated separately.

Make sure your content is well-structured with clear headings and paragraphs for optimal readability in both light and dark mode interfaces.
"""

# New prompt for generating decision points
DECISION_POINTS_PROMPT = """
Create a series of 3 decision points for a cybersecurity scenario titled "{scenario_title}" in the {scenario_domain} domain.
The decision points should be appropriate for someone in the {industry} industry with a {role} role and {experience_level} experience level.

Each decision point should:
1. Present a clear question related to the scenario
2. Offer 4 possible options/choices
3. Clearly mark which option is correct (only one option should be correct)
4. Increase in complexity/difficulty as they progress

IMPORTANT: Return ONLY the decision points in the following JSON format with no additional text, comments, or explanation:

[
  {{
    "question": "What action should you take when...",
    "options": [
      {{"text": "Option 1 description", "is_correct": false}},
      {{"text": "Option 2 description", "is_correct": true}},
      {{"text": "Option 3 description", "is_correct": false}},
      {{"text": "Option 4 description", "is_correct": false}}
    ]
  }},
  {{
    "question": "After the initial response, what should you do next...",
    "options": [
      {{"text": "Option 1 description", "is_correct": false}},
      {{"text": "Option 2 description", "is_correct": false}},
      {{"text": "Option 3 description", "is_correct": true}},
      {{"text": "Option 4 description", "is_correct": false}}
    ]
  }},
  {{
    "question": "To prevent this issue in the future, what measure would be most effective...",
    "options": [
      {{"text": "Option 1 description", "is_correct": false}},
      {{"text": "Option 2 description", "is_correct": false}},
      {{"text": "Option 3 description", "is_correct": false}},
      {{"text": "Option 4 description", "is_correct": true}}
    ]
  }}
]

Ensure the options are realistic, relevant to the {industry} industry, and the correct answer represents best security practices.
"""

# Prompt for generating a single decision point
DECISION_POINT_PROMPT = """
Create a single decision point (question #{decision_number}) for a cybersecurity scenario about {scenario_title} in the {scenario_domain} domain.
This is decision point #{decision_number} in the scenario.

The decision point should:
1. Present a clear question that follows naturally from the previous context
2. Offer 4 possible options/choices
3. Clearly mark which option is correct (only one option should be correct)
4. Be appropriate for someone in the {industry} industry with a {role} role and {experience_level} experience level
5. If this is a later decision point (3+), increase the complexity/difficulty

Format the decision point as HTML with a clear heading "Decision Point {decision_number}" and present the options as bullet points.

IMPORTANT: Return ONLY the decision point in the following JSON format with no additional text, comments, or explanation:

{{
  "question": "What action should you take when...",
  "options": [
    {{"text": "Option 1 description", "is_correct": false}},
    {{"text": "Option 2 description", "is_correct": true}},
    {{"text": "Option 3 description", "is_correct": false}},
    {{"text": "Option 4 description", "is_correct": false}}
  ],
  "html_content": "<h3>Decision Point {decision_number}</h3><p>What action should you take when...</p><ul><li>Option 1 description</li><li>Option 2 description</li><li>Option 3 description</li><li>Option 4 description</li></ul><p>Choose your response carefully, as it may impact the security of your organization.</p>"
}}

Ensure the options are realistic, relevant to the {industry} industry, and the correct answer represents best security practices.
"""

# Prompt for analyzing user decisions
DECISION_ANALYSIS_PROMPT = """
The user has made the following decision in response to a cybersecurity scenario about {scenario_description}:

User's decision: {user_decision}

This decision is {correctness}.

Provide a brief, concise analysis of this decision (50-75 words). Your analysis should:
1. Explain why the decision was good or problematic
2. Reference specific security principles relevant to the situation
3. Be educational without being condescending
4. Focus on practical implications
"""

# Prompt for generating learning moments
LEARNING_MOMENT_PROMPT = """
Create a concise learning moment related to the cybersecurity scenario about {scenario_description} in the {security_domain} domain.

The learning moment should:
1. Highlight 1-2 key security principles relevant to the scenario
2. Explain why these principles matter in practical terms
3. Provide 2-3 specific, actionable recommendations for improving security practices
4. Be approximately 100-150 words
5. Be formatted as HTML for better readability

Make the content educational, memorable, and directly applicable to real-world situations.
"""

# Prompt for assessment questions
ASSESSMENT_PROMPT = """
Create {num_questions} assessment questions related to the cybersecurity scenario titled "{scenario_title}".

The questions should:
1. Test understanding of key security concepts from the scenario
2. Include a mix of multiple-choice and short answer formats
3. Increase in difficulty
4. Be formatted with clear numbering and spacing

Format the assessment as HTML for better readability.
"""

# Prompt for generating recommendations
RECOMMENDATION_PROMPT = """
Based on the user's performance across cybersecurity scenarios, generate personalized recommendations 
for improving their security knowledge and practices.

The user has shown strengths in: {strengths}
The user has shown knowledge gaps in: {knowledge_gaps}

Provide 3-5 specific, actionable recommendations that:
1. Address the identified knowledge gaps
2. Build upon existing strengths
3. Are relevant to their industry ({industry}) and role ({role})
4. Include specific resources or exercises when appropriate

Format the recommendations as a bulleted HTML list for readability.
"""

# Prompt for generating knowledge assessment
KNOWLEDGE_ASSESSMENT_PROMPT = """\
Create a knowledge assessment for a cybersecurity scenario with the following details:

Scenario Title: {scenario_title}
Domain: {scenario_domain}
User's Industry: {user_industry}
User's Role: {user_role}
User's Experience Level: {experience_level}
Number of Questions: {num_questions}

Generate exactly {num_questions} multiple-choice questions that test the user's understanding of cybersecurity concepts related to the scenario domain. Each question should have 4 options with exactly one correct answer.

The assessment should be tailored to the user's industry, role, and experience level.

Format your response as a JSON object with the following structure:
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": [
        {{"text": "Option 1", "is_correct": false}},
        {{"text": "Option 2", "is_correct": true}},
        {{"text": "Option 3", "is_correct": false}},
        {{"text": "Option 4", "is_correct": false}}
      ],
      "explanation": "Explanation of why the correct answer is right and why others are wrong."
    }},
    // More questions...
  ]
}}

Make sure the questions:
1. Are relevant to the scenario domain
2. Test practical knowledge that would be useful in the user's role
3. Cover different aspects of the domain (prevention, detection, response, etc.)
4. Are at an appropriate difficulty level for the user's experience
5. Include clear explanations for each correct answer
"""
