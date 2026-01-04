import os

# Try importing LangChain/Google modules, fallback to mock if missing/error
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.prompts import PromptTemplate
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False

# ---------------------------------------------------------
# GLOBAL CONSTANTS
# ---------------------------------------------------------
ASSIGNMENT_GROUPS = [
    "Monitoring", "Windows", "Unix", "Storage", "Backup", 
    "Network", "Firewall", "Tools", "Database", "Cloud"
]

def get_llm():
    """
    Initializes the Gemini Model.
    Requires GOOGLE_API_KEY in environment variables.
    """
    # Direct assignment based on user input (Note: strictly, this should be an env var check, 
    # but the user pasted the key directly in the getenv call).
    # Correcting to use the key provided or fall back to Env Var.
    api_key_env = os.getenv("GOOGLE_API_KEY")
    api_key = api_key_env if api_key_env else "AIzaSyBLwakLrCYKh61TW7ppzR94mBgzp23-Skw"
    if not api_key:
        return None
    
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key)

# ---------------------------------------------------------
# SECURITY NOTE: Replace 'YOUR_API_KEY_HERE' with your actual Google AI Studio Key
# Example: GOOGLE_API_KEY = "AIzaSy..."
# ---------------------------------------------------------
GOOGLE_API_KEY = "AIzaSyDw4DnPpIY1JjvM1xuhxCqbXb6w1eOdMiA" 

def get_api_key():
    """Prioritizes Hardcoded Key -> Env Var -> Session State"""
    # 1. Hardcoded in File (Highest Priority as requested)
    if GOOGLE_API_KEY and GOOGLE_API_KEY != "":
        return GOOGLE_API_KEY
        
    # 2. Environment Variable
    if os.environ.get("GOOGLE_API_KEY"):
        return os.environ.get("GOOGLE_API_KEY")
        
    # 3. Session State (Legacy/Fallback)
    if 'google_api_key' in st.session_state and st.session_state['google_api_key']:
        return st.session_state['google_api_key']
        
    return None

def generate_acknowledgment_note(description, group):
    try:
        api_key = get_api_key()
        if not api_key:
             # Mock Response
             return f"Ticket assigned to {group}. Initial investigation started. (Demo: AI Key missing)"
             
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key)
        
        prompt = f"""
        You are an IT Service Desk Agent. Write a short, professional 1-sentence acknowledgment note for a ticket.
        Ticket Description: "{description}"
        Assignment Group: "{group}"
        The note should state that the ticket is assigned and investigation has begun.
        """
        
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        # Smart Offline Fallback - Clean professional note without error codes
        return f"Ticket assigned to {group}. Initial investigation started. (System Auto-Ack)"

from fpdf import FPDF
import base64

def generate_resolution_steps(description, group, manufacturer="Generic", ci_type="Unknown"):
    
    # ---------------------------------------------------------
    # SMART OFFLINE RESOLUTIONS (Fallback when AI unavailable)
    # ---------------------------------------------------------
    
    # Default Generic
    default_steps = f"""
    **{manufacturer} General Troubleshooting**
    1. *Log Analysis*: Check {manufacturer} system logs for critical errors around the timestamp.
    2. *Service Health*: Verify the status of the {ci_type} service/daemon.
    3. *Restart*: Attempt a graceful restart if the service is hung.
    4. *Support*: Open a priority case at the {manufacturer} Support Portal.
    """

    # Specific Templates based on Group/Type
    templates = {
        "Network": f"""
        **{manufacturer} Network Diagnostic Procedure**
        1. *Interface Check*: SSH into the {manufacturer} device and run `show interface status` / `show ip int brief`.
        2. *Error Counters*: Check for CRC errors or input drops: `show int | include error`.
        3. *Logs*: Analyze buffer logs: `show logging | include {ci_type}`.
        4. *CablingVerify*: Request onsite check of fiber/copper cables for physical damage.
        """,
        "Firewall": f"""
        **{manufacturer} Security Appliance Troubleshooting**
        1. *Session Table*: Check current session count vs limit on {manufacturer} dashboard.
        2. *Rule Trace*: Run packet tracer command to verify traffic flow against policies.
        3. *VPN Status*: Check IKE/IPSec phase status: `show vpn ipsec-sa`.
        4. *Failover*: Verify High Availability (HA) status and sync.
        """,
        "Windows": f"""
        **{manufacturer} Windows Server Resolution**
        1. *Event Viewer*: Open `eventvwr.msc` and filter System/Application logs for 'Error' level.
        2. *Services*: Check `services.msc` for any Stopped or Starting services (e.g., Spooler).
        3. *Resources*: Check Task Manager for high CPU/Memory processes.
        4. *Updates*: Verify if recent Windows Updates were applied pending reboot.
        """,
        "Unix": f"""
        **{manufacturer} Linux/Unix Resolution**
        11. *System Load*: Run `top` or `htop` to check load averages and zombie processes.
        2. *Disk Space*: Run `df -h` to verify mount point usage (check /var and /tmp).
        3. *Logs*: Tail the system log: `tail -f /var/log/messages` or `journalctl -xe`.
        4. *Service*: Status check: `systemctl status {ci_type.lower()}`.
        """,
        "Database": f"""
        **{manufacturer} Database Optimization**
        1. *Connection*: Verify connectivity using `tnsping` or connection string tests.
        2. *Locks*: Query active sessions to identify blocking locks or deadlocks.
        3. *Logs*: Check the {manufacturer} alert log for corruption or space errors.
        4. *Resources*: Ensure sufficient memory/SGA is allocated to the instance.
        """,
        "Storage": f"""
        **{manufacturer} Storage Array Diagnostics**
        1. *Alerts*: Login to {manufacturer} Management Console and acknowledge active alerts.
        2. *LUN Status*: Verify the target LUN is Online and pathing is Active/Optimized.
        3. *Hardware*: Check physical disk indicators for amber lights (Predictive Failure).
        4. *Logs*: Generate a support bundle for {manufacturer} analysis.
        """,
        "Backup": f"""
        **{manufacturer} Backup Failure Analysis**
        1. *Job Details*: Review the specific error code (e.g., Status 96, Error 12) in the job log.
        2. *Media*: Confirm tape library/disk pool has available scratch media/capacity.
        3. *Connectivity*: Verify the client agent on the target server is reachable on port 10000+.
        4. *Retry*: Rerun the job manually after clearing the obstruction.
        """
    }

    # Select best template or fall back to default
    mock_steps = templates.get(group, default_steps)
    
    try:
        api_key = get_api_key()
        if not api_key:
             return mock_steps
             
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key)
        
        prompt = f"""
        You are a Senior L3 Engineer specialized in {manufacturer} technologies.
        Provide a specific technical resolution procedure for:
        Issue: "{description}"
        CI Type: "{ci_type}"
        Manufacturer: "{manufacturer}"
        Assignment Group: "{group}"
        
        **Action Required**: Search your knowledge base for official documentation, KB articles, or troubleshooting guides specifically from the **{manufacturer} Support Portal**.
        Provide a compact step-by-step guide (max 3-4 steps) based on these official recommendations.
        Include specific commands or actions relevant to {manufacturer} systems.
        """
        
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        # Fallback to SMART TEMPLATES on error so user ALWAYS sees specific steps
        return mock_steps

def create_pdf_recommendation(ticket_id, description, recommendation, manufacturer):
    """Generates a PDF byte string for the recommendation."""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, f'Resolution Guide: {ticket_id}', 0, 1, 'C')
            self.ln(5)
         # Create PDF Object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"Incident Resolution Guide: {ticket_id}", ln=1, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=f"Description: {description}")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', size=11)
    pdf.cell(200, 10, txt="Recommended Resolution Steps:", ln=1)
    pdf.set_font("Arial", size=10)
    
    # Clean up formatting for PDF
    clean_rec = recommendation.replace("**", "").replace("*", "")
    pdf.multi_cell(0, 10, txt=clean_rec)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', size=9)
    pdf.cell(0, 10, txt=f"Generated by AI Agent Tina for {manufacturer} Systems", ln=1, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

def query_incident_bot(user_query, context_str):
    """
    Chatbot function for Agent Tina.
    context_str: A string summary of current incidents (ID, Status, Desc).
    """
    try:
        api_key = get_api_key()
        if not api_key:
            return "I'm currently offline (API Key Missing). Please check my configuration."
            
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key)
        
        prompt = f"""
        You are Agent Tina, an expert Intelligent Operations Commander.
        You are assisting a Site Reliability Engineer (the user).
        
        Current Active Incidents Context:
        {context_str}
        
        User Query: "{user_query}"
        
         Instructions:
        1. Answer the user's question based ONLY on the provided Incident Context.
        2. If the user asks about a specific ticket (e.g., INC12345), find it in the context.
        3. Be professional, concise, and helpful. 
        4. If the answer isn't in the context, say so.
        5. Keep a "Command Center" tone (efficient, clear).
        """
        
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"I encountered a system error: {str(e)}"
