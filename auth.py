import streamlit as st
import time
import base64

def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def init_user_db():
    if 'users_db' not in st.session_state:
        # Default admin user
        st.session_state['users_db'] = {"admin": "admin"}

def check_credentials(username, password):
    init_user_db()
    db = st.session_state['users_db']
    return username in db and db[username] == password

def set_bg_and_style():
    # Set Background Image for Login Page
    try:
        img_b64 = get_base64_bin_file("telefonica_o2_login_v2.png")
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* White Glass Overlay for the Form Column to make it readable */
        div[data-testid="stForm"] {{
            background: rgba(255, 255, 255, 0.9) !important;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        /* Link Button Styling */
        .auth-link {{
            background: none!important;
            border: none;
            padding: 0!important;
            color: #1e3a8a !important;
            text-decoration: underline;
            cursor: pointer;
            border-bottom: 1px solid #1e3a8a;
        }}
        </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        pass

def _render_login():
    col1, col2 = st.columns([3, 2]) 
    
    with col2:
        st.write("") # Top Spacer
        st.write("")
             
        st.markdown("<h1 style='text-align: left; color: #1e3a8a;'>Incident Commander</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: left; color: #64748b;'>Login to continue</h4>", unsafe_allow_html=True)
        
        # Using a form to handle Enter key submission
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            st.write("")
            submit_button = st.form_submit_button("Login", use_container_width=False)
            
            if submit_button:
                if check_credentials(username, password):
                    st.success("Login Successful!")
                    time.sleep(0.5)
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        
        # Navigation Links
        col_signup, col_forgot = st.columns(2)
        with col_signup:
            if st.button("Start a new account", key="go_signup"):
                st.session_state['auth_page'] = 'signup'
                st.rerun()
        with col_forgot:
            if st.button("Forgot Password?", key="go_reset"):
                st.session_state['auth_page'] = 'reset'
                st.rerun()

def _render_signup():
    col1, col2 = st.columns([3, 2]) 
    with col2:
        st.write("")
        st.write("")
        st.markdown("<h1 style='text-align: left; color: #1e3a8a;'>Create Account</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: left; color: #64748b;'>Join the Ops Commander</h4>", unsafe_allow_html=True)
        
        with st.form("signup_form"):
            new_user = st.text_input("Choose Username")
            new_pass = st.text_input("Choose Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            
            st.write("")
            if st.form_submit_button("Sign Up", use_container_width=False):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match!")
                elif not new_user or not new_pass:
                    st.error("Please fill all fields")
                else:
                    # Save to In-Memory DB
                    init_user_db()
                    if new_user in st.session_state['users_db']:
                        st.error("Username already exists!")
                    else:
                        st.session_state['users_db'][new_user] = new_pass
                        st.success("Account created! Please log in.")
                        time.sleep(1)
                        st.session_state['auth_page'] = 'login'
                        st.rerun()
                    
        if st.button("← Back to Login", key="back_login_1"):
            st.session_state['auth_page'] = 'login'
            st.rerun()

def _render_reset():
    col1, col2 = st.columns([3, 2]) 
    with col2:
        st.write("")
        st.write("")
        st.markdown("<h1 style='text-align: left; color: #1e3a8a;'>Recovery</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: left; color: #64748b;'>Reset your password</h4>", unsafe_allow_html=True)
        
        with st.form("reset_form"):
            email = st.text_input("Enter your Email/Username")
            
            st.write("")
            if st.form_submit_button("Send Reset Link", use_container_width=False):
                if email:
                    st.success(f"Recovery link sent to {email} (Simulated)")
                else:
                    st.error("Please enter an email")
                    
        if st.button("← Back to Login", key="back_login_2"):
            st.session_state['auth_page'] = 'login'
            st.rerun()

def login_ui():
    # Ensure state exists
    if 'auth_page' not in st.session_state:
        st.session_state['auth_page'] = 'login'
        
    set_bg_and_style()
    
    if st.session_state['auth_page'] == 'login':
        _render_login()
    elif st.session_state['auth_page'] == 'signup':
        _render_signup()
    elif st.session_state['auth_page'] == 'reset':
        _render_reset()
