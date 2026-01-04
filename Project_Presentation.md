# Project Presentation: AI Agent Tina

---

## Slide 1: Title Slide

# AI Agent Tina
### Intelligent Incident Operations Commander

**Presented by**: [Your Name/Team]
**Date**: 2026

---

## Slide 2: The Problem
### The Challenge of Modern IT Ops

*   **High Volume**: Support teams are overwhelmed by thousands of alerts daily.
*   **Slow Response**: Human analysis takes time (15-20 mins per ticket).
*   **Inconsistency**: Different engineers solve the same problem in different ways.
*   **Burnout**: Repetitive L1 tasks drain morale.

---

## Slide 3: The Solution
### Meet Agent Tina

A **Next-Gen Incident Management System** powered by Generative AI.

*   **Automated**: Instantly acknowledges and assigns tickets.
*   **Intelligent**: Uses Google Gemini 1.5 to analyze issues like a Senior Engineer.
*   **Interactive**: Real-time Voice & Visual feedback.
*   **Resilient**: "Smart Offline" mode ensures operations never stop.

---

## Slide 4: Key Features

1.  **Auto-Assignment Engine**:
    *   Round-robin logic based on live Shift Rosters.
    *   Respects "Week Off" and "Leave" status.

2.  **AI Analysis (Gemini 1.5 Flash)**:
    *   Generates professional acknowledgment notes.
    *   Creates **PDF Resolution Guides** with specific command-line steps.

3.  **Command Center Dashboard**:
    *   Live countdown timer for batch processing.
    *   Audio/TTS notifications ("Agent Tina speaking...").
    *   Real-time chat Copilot for status queries.

---

## Slide 5: System Architecture

*   **Frontend**: Streamlit (Python) - *Chosen for rapid interactive UI.*
*   **Backend Logic**: Python (Pandas) - *Robust data handling.*
*   **AI Engine**: Google Vertex AI / LangChain.
*   **Deployment**: Lightweight, container-ready, secure.

---

## Slide 6: Demo Scenario

**What you will see today:**

1.  **Generation**: We simulate a storm of network & server alerts.
2.  **Reaction**: Watch Agent Tina wake up, analyze, and assign tickets in <10 seconds.
3.  **Resolution**: We will open a generated PDF guide to see L3-level troubleshooting steps.
4.  **Interaction**: We will ask the Tina Chatbot about the live situation.
