# 💻 Technology Stack

## Core Framework
- **[Python 3.10+](https://www.python.org/)**: The primary programming language.
- **[Streamlit](https://streamlit.io/)**: The web framework used to build the interactive dashboard and UI. It handles the frontend rendering and backend logic in a unified script.

## Artificial Intelligence (AI)
- **[Google Gemini 1.5 Flash](https://deepmind.google/technologies/gemini/)**: A high-performance multimodal model used for:
    - Analyzing incident descriptions.
    - Categorizing tickets (CI Type, Manufacturer).
    - Generating step-by-step resolution guides.
    - Creating human-like acknowledgment notes.
- **`google-generativeai` SDK**: The Python client library for accessing Gemini APIs.

## Data Management
- **[Pandas](https://pandas.pydata.org/)**: Used extensively for:
    - Managing the Incident Database (DataFrame).
    - Handling Shift Rosters (CSV parsing, filtering).
    - Data manipulation for dashboard stats.

## PDF Generation
- **[FPDF](https://pyfpdf.readthedocs.io/en/latest/)**: A lightweight library used to programmatically generate PDF Resolution Guides containing the AI's recommendations.

## Frontend & Interaction
- **HTML/CSS**: Custom CSS is injected via `st.markdown` to style the dashboard (Telefonica Midnight theme, animations, glassmorphism).
- **JavaScript**: Injected via `st.components.v1.html` to handle:
    - **Web Speech API**: For the "Tina" voice synthesis.
    - **AudioContext**: For the countdown "tick" sound.

## Environment Management
- **`python-dotenv`**: Loads configuration secrets (API Keys) from `.env` files securely.
