# AI Concepts and Logic

## 1. AI Model Overview
The system relies on **Google Gemini 1.5 Flash** as its intelligence engine. This model was chosen for its balance of high speed (low latency) and reasoning capability, which is crucial for real-time dashboard updates.

*   **Model Name**: `gemini-1.5-flash-latest`
*   **Integration Method**: `langchain-google-genai` library.
*   **Authentication**: Secure API calls using `GOOGLE_API_KEY`.

## 2. Core AI Functions
The AI is embedded in three specific workflows within `llm_utils.py`:

### A. Automatic Ticket Acknowledgment
*   **Goal**: Generate a professional, short, human-like acknowledgment note for new tickets.
*   **Mechanism**: A "One-shot" prompt is sent to the LLM with the ticket description and assignment group.
*   **Output**: A single sentence string (e.g., *"Monitoring Team has received ticket INC123 regarding high CPU load and has started investigation."*)

### B. Intelligent Resolution Guide (PDF)
*   **Goal**: Provide L3-level troubleshooting steps for specific manufacturers (Cisco, Microsoft, Oracle, etc.).
*   **Prompt Logic**: The system constructs a prompt dynamically injecting:
    *   Incident Description
    *   Configuration Item (CI) Type
    *   Manufacturer
    *   Assignment Group
*   **Contextual Role**: The AI is instructed to act as a *"Senior L3 Engineer"* and strictly look for *"official documentation"* style answers.

### C. "Agent Tina" Chatbot
*   **Goal**: Context-aware Q&A about active incidents.
*   **RAG-Lite Approach**:
    *   The system acts as a basic RAG (Retrieval-Augmented Generation) by injecting the **current session state of incidents** (ID, Status, Description) directly into the prompt context.
    *   This allows the user to ask "How many tickets are assigned to Network?" and the AI answers based on real-time data without needing a vector database.

## 3. The "Smart Offline" Fallback Logic
A critical architectural decision is the **Deterministic Fallback Layer**. If the AI service is unavailable (API error, Internet down, Missing Key), the system **does not fail**.

Instead, it switches to specific hardcoded templates based on the Assignment Group:
*   **Network**: Checks interfaces, error counters, cables.
*   **Windows**: checks Event Viewer, services.msc.
*   **Cloud**: Checks quotas, health dashboard.

This ensures the user *always* gets a generated PDF with valid troubleshooting steps, even without the LLM.

## 4. Prompt Engineering Strategy
The prompts utilize **Persona-Based Interaction**:
*   *"You are an IT Service Desk Agent..."*
*   *"You are a Senior L3 Engineer..."*
*   *"You are Agent Tina, an expert Intelligent Operations Commander..."*

This primes the model to adopt the correct tone (Professional, Technical, or Command-Center style) relevant to the task.
