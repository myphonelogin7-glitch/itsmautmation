# 🏗️ System Architecture & Application Flow

## 📐 System Architecture

The application is built on a **Streamlit** (Python) framework, integrating various components for logic, AI, and user interaction.

```mermaid
graph TD
    User[User / Browser] <-->|Interacts| StreamlitApp[Streamlit App (app.py)]
    
    subgraph "Core Modules"
        StreamlitApp --> Auth[auth.py]
        StreamlitApp --> Dash[dashboard.py]
        StreamlitApp --> Incidents[incidents.py]
        StreamlitApp --> Roster[roster.py]
        StreamlitApp --> LLM[llm_utils.py]
    end

    subgraph "External Services / APIs"
        LLM -->|API Call| GoogleGemini[Google Gemini 1.5 Flash]
        Dash -->|JS Injection| WebSpeech[Browser Speech Synthesis]
    end

    subgraph "Data Storage"
        Incidents <-->|Read/Write| SessionState[st.session_state (In-Memory)]
        Roster <-->|Read/Write| SessionState
    end
```

### Components
- **`app.py`**: Main entry point, handles global styling (CSS) and routing.
- **`dashboard.py`**: Renders the main UI, manages the auto-assign timer, and handles client-side effects (Audio/Toasts).
- **`incidents.py`**: Core logic for generating mock tickets, processing them, and determining assignments.
- **`roster.py`**: Manages shift data, personnel lookups, and "Day of Week" logic.
- **`llm_utils.py`**: Interface for Google Gemini API to generate intelligent context for tickets.

---

## 🔄 Application Flow

### 1. Incident Generation
1.  User selects "Generate Incidents".
2.  `incidents.trigger_incidents()` creates mock data rows.
3.  Tickets are added to `st.session_state['incidents_df']` with status `New`.

### 2. Auto-Assignment Loop
1.  **Timer**: The dashboard countdown reaches 0.
2.  **Trigger**: `incidents.process_tickets()` is called.
3.  **Processing (Per Ticket)**:
    - **Step A**: Analyze Description (LLM).
    - **Step B**: Determine Assignment Group.
    - **Step C**: **Roster Lookup** (`roster.get_personnel_for_group`).
        - Checks today's date and shift.
        - Filters out "WO" (Week Off) or "Leave".
        - Selects assignee via Round-Robin.
    - **Step D**: Update Status to `Assigned` (or `In Progress`).
    - **Step E**: Generate PDF Resolution Guide.

### 3. Notification & Feedback
1.  **Server-Side**: Python constructs a "Feedback" object containing:
    - Assignee Name
    - Voice Message Text ("Hi [Name]...")
    - Notification Flags (Email=True, Teams=True)
2.  **Client-Side (Dashboard)**:
    - **Spinner**: Shows "Agent Tina is notifying [Name]..."
    - **Voice**: Injects JavaScript to speak the message.
    - **Toasts**: Displays sequential popups for Assignment, Email, and Teams.
    - **Wait**: Pauses for 2.5s to ensure audio completion.

### 4. Completion
- Once all tickets are processed, the status updates to "All incidents processed!" and the loop ends.
