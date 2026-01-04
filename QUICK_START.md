# ⚡ Quick Start Guide

Follow these steps to set up and run the AI Agent Tina Incident Management System.

## 📋 Prerequisites

- **Python 3.10+** installed on your system.
- A **Google Gemini API Key** (for LLM features).

## 🛠️ Installation

1.  **Clone the Repository** (or download the source code):
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Install Dependencies**:
    Create a `requirements.txt` file (if not present) with the following:
    ```
    streamlit
    pandas
    google-generativeai
    fpdf
    python-dotenv
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory and add your API key:
    ```env
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

## 🚀 Running the Application

Execute the Streamlit application:

```bash
streamlit run app.py
```

The application will launch in your default web browser (usually at `http://localhost:8501`).

## 📖 Usage Guide

### 1. Login
- Use the default credential (or sign up if enabled).
- **Default User**: `admin` / `admin` (if configured in `auth.py`).

### 2. Dashboard Overview
- View **Active Incidents** and **Assignment Groups** immediately.
- A **Countdown Timer** (red text) indicates when the next auto-assignment batch will run.

### 3. Generating Incidents
- Go to the **"Incident Simulation Trigger"** section.
- Select source (Event/User), Count (e.g., 5), and Target Group.
- Click **"Generate Incidents"**.

### 4. Assignment Process
- Wait for the countdown to reach 0.
- **Tina** will verbally announce updates.
- **Popups** will confirm:
    1.  Calculated Assignment
    2.  Email Sent
    3.  Teams Message Sent

### 5. Shift Roster
- Navigate to "Shift Roster" in the sidebar.
- Upload a custom CSV or generate a **Mock Roster**.
- Ensure today's date has coverage to avoid "No Personnel Found" errors.
