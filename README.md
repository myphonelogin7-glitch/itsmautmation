# 🛡️ AI Agent Tina - Intelligent Incident Management System

**AI Agent Tina** is a next-generation automated incident management dashboard designed to streamline IT Operations. It leverages generative AI, voice synthesis, and intelligent automation to analyze, assign, and resolve incidents with minimal human intervention.

![Dashboard Preview](dashboard_preview.png) *(Note: Add a screenshot here)*

## 🌟 Key Features

### 🧠 Intelligent Analysis
- **Auto-Triage**: Uses **Google Gemini 1.5 Flash** to analyze incident descriptions, determine CI types, and recommend resolution steps.
- **Root Cause Analysis**: Automatically generates comprehensive resolution guides in PDF format.

### 🗣️ Interactive Voice Assistant ("Tina")
- **Voice Notifications**: "Tina" verbally announces assignments with a soft, professional female voice.
- **Personalized Messages**: *"Hi [Name], a new incident has been assigned to your name..."*
- **Updates**: Provides audible status updates during the analysis process.

### ⚡ Automated Assignment Flow
- **Smart Routing**: Checks the **Shift Roster** to find available personnel for specific assignment groups (Database, Network, Server, etc.).
- **Round-Robin logic**: Distributes tickets evenly among available staff.
- **Roster Awareness**: intelligently handles "Week Off" (WO) and "Leave" statuses to ensure coverage.

### 🔔 Omni-Channel Notifications (Simulated)
- **Toast Popups**: Visual confirmation of assignment.
- **Email Simulation**: "📧 Email sent to [User]" feedback.
- **Teams Integration**: "💬 Teams message sent to [User]" feedback.

### 📊 Real-Time Dashboard
- **Live Counters**: Track Active Incidents.
- **Countdown Timer**: Auto-assignment trigger with audible "tick" sound.
- **Visual Status**: Color-coded priorities (Critical, High, Medium, Low) and statuses.

## 🚀 Getting Started

See [QUICK_START.md](QUICK_START.md) for installation and usage instructions.

## 🏗️ Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for system design and application flow.

## 💻 Technology Stack

See [TECHNOLOGY.md](TECHNOLOGY.md) for details on libraries and frameworks used.
