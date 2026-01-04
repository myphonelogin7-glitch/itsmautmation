# Project Structure & File Dictionary

This document provides a comprehensive overview of the **AI Agent Tina** codebase.

## 📁 Root Directory (`/`)

### Core Application
| File | Description |
| :--- | :--- |
| **`app.py`** | **Entry Point**. Initializes the Streamlit app, handles global CSS/Theming, authentication checks, and routing between Dashboard and Roster views. |
| **`dashboard.py`** | **Main UI**. Contains the Incident Operations Center. Manages the "Auto-Assign" timer loop, plays audio notifications, and renders the live incident table. |
| **`incidents.py`** | **Business Logic**. Handles generating mock incidents, processing them (assigning groups), and managing the core dataframes in `st.session_state`. |
| **`roster.py`** | **Resource Management**. Defines the shift schedule (Day/Night), personnel lists per group, and logic to check if a person is "On Shift" or "Week Off". |
| **`auth.py`** | **Security**. A lightweight authentication module handling Login/Signup forms and storing user credentials in session state. |

### AI Integration
| File | Description |
| :--- | :--- |
| **`llm_utils.py`** | **Intelligence Layer**. Interacts with Google Gemini API. Contains prompts for Ticket Acknowledgment, Resolution Generation, and the Chatbot. Use this to configure API Keys. |
| **`diagnose_models.py`** | *(Utility)* Setup script for identifying or diagnosing model availability (Currently a placeholder). |

### Configuration & Assets
| File | Description |
| :--- | :--- |
| **`requirements.txt`** | **Dependencies**. List of Python libraries required to run the app. |
| **`tina_avatar.png`** | **Asset**. The avatar image used in the main banner for "Agent Tina". |
| **`background.png`** | **Asset**. Background images used for login screens or themes. |

## 📚 Documentation
| File | Description |
| :--- | :--- |
| `ARCHITECTURE.md` | High-level system design diagram/flow. |
| `Technical_Specifications.md` | Detailed tech stack, data flow, and deployment specs. |
| `AI_Concepts_and_Logic.md` | Deep dive into how the AI prompts and fallback logic work. |
| `Demo_Guide.md` | Step-by-step instructions for presenting the application. |
| `Troubleshooting.md` | Solutions for common installation or runtime errors. |
