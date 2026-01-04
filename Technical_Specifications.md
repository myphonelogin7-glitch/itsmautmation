# Technical Specifications

## 1. System Overview
The **AI Agent Tina - Incident Management System** is a python-based web application designed to simulate and manage IT operations. It utilizes **Streamlit** for the frontend and **Google Gemini 1.5 Flash** (via LangChain) for intelligent incident analysis and resolution generation.

## 2. Architecture
The system follows a modular architecture where the frontend triggers backend logic for incident generation, processing, and personnel assignment.

**Key Components:**
*   **Frontend**: Streamlit App (`app.py`, `dashboard.py`)
*   **Logic Layer**: Incident generation (`incidents.py`), Roster management (`roster.py`)
*   **AI Layer**: LLM Integration (`llm_utils.py`)
*   **Data**: In-memory `st.session_state` (Non-persistent)

### Data Flow
1.  **User Action**: Triggers incident generation.
2.  **State Update**: Incidents stored in session state.
3.  **Automation**: Timer triggers processing loop.
4.  **AI Analysis**: Incident description sent to Gemini API -> Returns Analysis/Resolution.
5.  **assignment**: System checks `roster.py` for available agents.
6.  **Notification**: UI updates with assignments and visual/audio feedback.

## 3. Technology Stack

### Core Frameworks
*   **Language**: Python 3.x
*   **Web Framework**: Streamlit
*   **AI orchestration**: LangChain (Google GenAI)

### Key Libraries
| Library | Purpose |
| :--- | :--- |
| `streamlit` | Main web application framework |
| `langchain-google-genai` | Interface for Google Gemini API |
| `langchain` | Prompt templates and chain management |
| `fpdf` | PDF generation for resolution guides |
| `watchdog` | File system monitoring (Streamlit dependency) |
| `python-dotenv` | Environment variable management (Recommended) |

### AI Service
*   **Provider**: Google Vertex AI / AI Studio
*   **Model**: `gemini-1.5-flash-latest`
*   **Auth**: API Key (Environment Variable `GOOGLE_API_KEY`)

## 4. Directory Structure
```
/
├── app.py                 # Entry point, routing, auth, styling
├── dashboard.py           # Main dashboard UI, timer logic
├── incidents.py           # Ticket generation and processing logic
├── roster.py              # Shift management and personnel logic
├── llm_utils.py           # GEMINI API integration & prompt engineering
├── auth.py                # Simple login/authentication mechanism
├── diagnose_models.py     # (Placeholder) Diagnostic tool
├── requirements.txt       # Project dependencies (See Section 5)
└── assets/                # Images (tina_avatar.png, etc.)
```

## 5. Deployment Requirements

### Environment Variables
The application requires the following environment variables to be set:
*   **`GOOGLE_API_KEY`**: Valid Google AI Studio API Key for Gemini.

### Installation
(If `requirements.txt` is missing, create it with the following content)
```text
streamlit
langchain-google-genai
langchain
fpdf
watchdog
python-dotenv
```

## 6. Security Considerations
*   **API Key Storage**: Currently, the system looks for a hardcoded key in `llm_utils.py` as a fallback. **This is a security risk.** Recommendation: Remove hardcoded keys and strictly enforce `os.environ`.
*   **Authentication**: Basic hardcoded/session-based auth in `auth.py`. Not suitable for production without integration into an SSO provider.
