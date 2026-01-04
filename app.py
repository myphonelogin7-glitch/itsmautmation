import streamlit as st
import auth
import dashboard
import roster
import incidents

# Set Page Configuration
st.set_page_config(
    page_title="Incident Management System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# GLOBAL VISUAL THEME (Telefonica Midnight)
# -----------------------------------------------------------------------------
# Removed Background Image Logic as per request
background_style = """
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    background-size: cover;
    background-attachment: fixed;
"""

st.markdown(f"""
<style>
    /* 0. Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* 1. Global Background (Light Theme Switch) */
    .stApp {{
        background: linear-gradient(135deg, #f0f2f5 0%, #ffffff 100%);
        color: #212529 !important; /* Dark Text */
    }}
    
    /* 2. Containers (White Cards with Shadow) */
    div[data-testid="stMetric"], 
    div[data-testid="stExpander"], 
    div[data-testid="stPopover"],
    .stDataFrame,
    .banner-container,
    div[data-testid="stForm"] {{
        background: #ffffff !important;
        border: 1px solid rgba(0,0,0,0.1);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        color: #212529 !important;
    }}
    
    /* 3. Text Visibility in Cards */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {{
        color: #0f172a !important; /* Navy Blue Headers */
    }}
    
    /* 4. Sidebar (Midnight Blue - Reverted as per Screenshot) */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0f0a2e 0%, #15002b 100%) !important;
        border-right: 1px solid rgba(147, 51, 234, 0.3);
    }}
    
    /* Force White Text in Sidebar for Contrast against Dark Background */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] div, 
    section[data-testid="stSidebar"] label {{
        color: #ffffff !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.8);
    }}
    
    /* Sidebar Radio Button Styling */
    section[data-testid="stSidebar"] .stRadio label {{
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }}
    
    /* 5. Inputs (Light Background, Dark Text) */
    .stTextInput > div > div, 
    .stNumberInput > div > div, 
    .stSelectbox > div > div, 
    .stDateInput > div > div {{
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
    }}
    
    /* FIX: Force Input Text and Icons to be Dark (overriding Sidebar White) */
    .stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox div[data-testid="stMarkdownContainer"] {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        caret-color: #000000 !important;
    }}
    /* Force Icons (Magnifying glass, Arrow) to be dark */
    .stTextInput svg, .stSelectbox svg, .stNumberInput svg {{
         fill: #000000 !important;
         color: #000000 !important;
    }}
    /* Dropdown List Items */
    ul[data-testid="stSelectboxVirtualDropdown"] {{
         background-color: #ffffff !important;
         color: #000000 !important;
    }}
    
    input {{ color: #212529 !important; font-weight: bold; }}
    
    /* 6. Buttons (Midnight Blue -> Purple Gradient) */
    /* 6. Buttons (Midnight Blue -> Purple Gradient) */
    /* 6. Buttons (Midnight Blue -> Purple Gradient) */
    .stButton>button, .stDownloadButton>button {{
        background: linear-gradient(90deg, #191970 0%, #800080 100%); /* Midnight -> Purple */
        color: white !important;
        font-weight: bold;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    /* FIX: Force text inside buttons (often <p> tags) to be white, overriding global p style */
    .stButton>button p, .stDownloadButton>button p {{
        color: white !important;
    }}
    .stButton>button:hover, .stDownloadButton>button:hover {{
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(128, 0, 128, 0.6);
    }}
    
    /* 7. DataFrames (Light Theme) */
    div[data-testid="stDataFrame"] div[role="row"] {{
        background-color: #ffffff !important;
        color: #212529 !important;
        border-bottom: 1px solid #e2e8f0;
    }}
    div[data-testid="stDataFrame"] div[role="columnheader"] {{
        background: linear-gradient(90deg, #191970 0%, #800080 100%) !important; /* Gradient like Logout Button */
        color: white !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 4px;
    }}

    /* FIX: Force Black Text for generic Streamlit Popovers/Menus (DataFrame options, Selectbox options) */
    div[role="menu"], ul[role="listbox"], div[data-testid="stPopoverBody"] {{
        color: black !important;
        background-color: white !important;
         border: 1px solid #cbd5e1;
    }}
    div[role="menu"] div, ul[role="listbox"] li {{
        color: black !important;
    }}
    
    /* 8. Dataframe Toolbar (Top Right Actions) */
    div[data-testid="stElementToolbar"], div[data-testid="stToolbar"] {{
        background: linear-gradient(90deg, #191970 0%, #800080 100%) !important; /* Gradient Background */
        border-radius: 6px;
        color: white !important;
        opacity: 1 !important;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    div[data-testid="stElementToolbar"] button {{
        color: white !important;
        background: transparent !important;
    }}
    
    /* 9. Specific Input Contrast Fix (Select Year) */
    input[type="number"] {{
        color: #1e3a8a !important; /* Dark Blue for high visibility on light bg */
        font-weight: 800;
        text-shadow: none;
        background-color: #f1f5f9 !important; /* Force Light Background for Dark Text */
    }}
    

    
</style>
""", unsafe_allow_html=True)

def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Login'

def main():
    init_session_state()

    if not st.session_state['authenticated']:
        auth.login_ui()
    else:
        # -----------------------------------------------------------------------------
        # GLOBAL HEADER BANNER
        # -----------------------------------------------------------------------------
        st.markdown("""
        <style>
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(2deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }
        @keyframes glow {
            0% { text-shadow: 0 0 10px #00008B, 0 0 20px #00008B; opacity: 1; }
            50% { text-shadow: 0 0 20px #0000FF, 0 0 30px #0000FF; opacity: 0.9; }
            100% { text-shadow: 0 0 10px #00008B, 0 0 20px #00008B; opacity: 1; }
        }
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        .banner-container {
            background: linear-gradient(135deg, #191970 0%, #800080 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 3rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        /* Add a shimmer overlay */
        .banner-container::before {
            content: "";
            position: absolute;
            top: 0;
            left: -50%;
            width: 200%;
            height: 100%;
            background: linear-gradient(to right, transparent 0%, rgba(255,255,255,0.05) 50%, transparent 100%);
            transform: skewX(-25deg);
            animation: shimmer 6s infinite linear;
            pointer-events: none;
        }
        .avatar-img {
            height: 90px;
            margin-right: 20px;
            border-radius: 50%;
            box-shadow: 0 0 25px rgba(0, 247, 255, 0.6);
            border: 2px solid rgba(0, 247, 255, 0.3);
            animation: float 6s ease-in-out infinite;
        }
        .banner-title {
            margin: 0;
            font-size: 3.5rem;
            color: #ffffff !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 800;
            letter-spacing: 1px;
            animation: glow 3s ease-in-out infinite alternate;
        }
        .banner-subtitle {
            margin: 0;
            color: #191970 !important;
            font-size: 1.2rem;
            letter-spacing: 4px;
            text-transform: uppercase;
            font-weight: 800;
            text-shadow: 0 0 10px #ffffff, 0 0 20px #ffffff;
            position: relative;
            z-index: 1;
        }
        .title-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 2;
        }
        </style>
        """, unsafe_allow_html=True)

        # Load Banner Image
        try:
            import base64
            def get_base64_image(image_path):
                with open(image_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
            
            tina_img_b64 = get_base64_image("tina_avatar.png")
            icon_html = f'<img src="data:image/png;base64,{tina_img_b64}" class="avatar-img">'
        except FileNotFoundError:
            icon_html = '⚡' # Fallback if image not found
        except Exception as e:
            icon_html = '⚡' # General fallback for other errors
            st.error(f"Error loading Tina avatar: {e}")

        st.markdown(f"""
        <div class="banner-container">
            <div class="title-wrapper">
                {icon_html}
                <div style="text-align: left;">
                    <h1 class="banner-title">AI Agent Tina</h1>
                    <p class="banner-subtitle">INTELLIGENT OPS COMMANDER</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # -----------------------------------------------------------------------------
        
        # Sidebar Navigation
        with st.sidebar:
            st.title(f"Welcome, {st.session_state['username']}")
            st.divider()
            
            nav_selection = st.radio("Navigation", ["Dashboard", "Shift Roster"])
            
            st.divider()
            
            if st.button("Logout"):
                st.session_state['authenticated'] = False
                st.session_state['username'] = None
                st.rerun()

        # Page Routing
        if nav_selection == "Dashboard":
            dashboard.render_dashboard()
        elif nav_selection == "Shift Roster":
            roster.render_roster_page()

if __name__ == "__main__":
    main()
