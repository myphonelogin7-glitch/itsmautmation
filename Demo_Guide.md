# AI Agent Tina - Demo Guide

This guide covers the standard demonstration flow for the Incident Management System.

## 1. Preparation
Before the demo starts:
1.  Ensure Python and Streamlit are installed.
2.  Set the `GOOGLE_API_KEY` environment variable (or ensure a key is present in `llm_utils.py` for testing).
3.  Launch the application:
    ```bash
    streamlit run app.py
    ```

## 2. Login Flow
1.  Launch the app in your browser (usually `http://localhost:8501`).
2.  You will see the "Incident Commander" login screen.
3.  **Credential**: Use the default admin account:
    *   **Username**: `admin`
    *   **Password**: `admin`
4.  *(Optional)* Demonstrate the "Start a new account" flow to show user registration simulation.

## 3. Dashboard Walkthrough
Once logged in, you will see the **Command Center**.

### Step A: Incident Generation
1.  Locate the sidebar.
2.  Click the **"Generate Incidents"** button.
3.  **Observation**: 
    *   A table populates with 3-5 mock incidents (e.g., "Network Latency", "Database Connection Refused").
    *   Status is **New**.
    *   The "Auto-Assign" timer starts counting down (default 10s).

### Step B: Auto-Assignment & AI Processing
1.  **Wait** for the timer to hit 0.
2.  **Observation**:
    *   **Voice**: You will hear "Agent Tina" generated speech announcing assignment.
    *   **Visual**: Toast popups appear ("Assigning to [Group]...", "Sending Email...").
    *   **Status Update**: Tickets change from `New` -> `Assigned`.
    *   **Roster Logic**: Notice that specific names (e.g., "Alice", "Bob") are assigned based on the simulated shift roster.

### Step C: Resolution Guides (The "Wow" Factor)
1.  In the Incident Table, click on any **Ticket ID** (or the row).
2.  Click the **"Download Resolution PDF"** button.
3.  **Action**: Open the downloaded PDF.
4.  **Observation**:
    *   The PDF contains a professional header.
    *   It lists specific, AI-generated technical steps relevant to that ticket (e.g., Cisco commands for network issues, SQL queries for DB issues).

### Step D: Chat with Agent Tina
1.  Scroll to the **"Copilot"** section at the bottom.
2.  Type a question like: *"How many tickets are assigned to Network?"* or *"What is the issue with ticket INC1002?"*
3.  **Observation**: The chatbot replies with context-aware answers based on the current active table.

## 4. Shift Roster View
1.  In the Sidebar, switch navigation to **"Shift Roster"**.
2.  Show the calendar view and explain how the system determines who is "On Call" vs "Week Off".
