# CyberSaga: Immersive Cybersecurity Education Platform

CyberSaga transforms abstract security concepts into interactive, personalized adventures. By leveraging LLMs, intelligent AI agents, and an intuitive Streamlit interface, CyberSaga creates an engaging learning experience that adapts to each user's needs and learning style.

## Overview

CyberSaga takes users on narrative journeys through realistic cybersecurity scenarios where their decisions have meaningful consequences. Instead of passively consuming information about threats like phishing, ransomware, or social engineering, users become active participants in stories that teach practical security skills through experience.

## Features

- **Adaptive Narrative Engine**: Uses large language models to generate dynamic, branching security scenarios
- **Security Guide AI Agent**: Maintains narrative coherence while tracking learning objectives
- **Personalized Learning**: Adapts content based on the user's industry, role, and skill level
- **Multi-Perspective Learning**: Experience security scenarios from different viewpoints
- **Progress Tracking**: Dashboard showing security skills mastered and areas for improvement

## Getting Started

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Clone the repository
2. Create and activate a virtual environment (recommended)
3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

## Project Structure

- `app.py`: Main Streamlit application
- `agent.py`: Security Guide AI Agent implementation
- `scenarios.py`: Scenario classes and factory
- `user_profile.py`: User profile management
- `prompts.py`: Prompts for AI interactions

## Usage

1. Complete the onboarding process to personalize your experience
2. Select a cybersecurity scenario that interests you
3. Navigate through the scenario by making decisions
4. Receive feedback and learning moments based on your choices
5. Track your progress and skill development

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Streamlit
- Powered by Groq LLMs
- Agno framework for agent capabilities