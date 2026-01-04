import streamlit as st
import pandas as pd
from datetime import datetime
import llm_utils

def determine_current_shift():
    hour = datetime.now().hour
    if 6 <= hour < 14:
        return "Morning"
    elif 14 <= hour < 22:
        return "Afternoon"
    else:
        return "Night" 

def get_personnel_for_group(group_name):
    """
    Returns a list of available people for a given assignment group, 
    filtered by Current Date and Shift with fallback logic.
    """
    if 'roster_df' not in st.session_state or st.session_state['roster_df'].empty:
        return []

    df = st.session_state['roster_df'].copy()
    
    # Skip Header/Day-name rows (where Team Name is "None" or similar)
    df = df[df.iloc[:, 0].astype(str).str.lower() != "none"]
    
    # Standardize Column Names (Lowercase + Strip)
    df.columns = [str(c).lower().strip() for c in df.columns]
    
    # 1. Identify Critical Columns
    group_col = next((c for c in df.columns if any(k in c for k in ['assignment', 'group', 'team'])), None)
    person_col = next((c for c in df.columns if any(k in c for k in ['person', 'employee', 'staff', 'engineer', 'name']) and c != group_col), None)
            
    if not (group_col and person_col):
        return []

    # 2. Get Current Context
    now = datetime.now()
    # Broaden date variations to match substrings or exact dates
    current_date_variations = [now.strftime(fmt) for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d"]]
    current_shift = determine_current_shift().lower().strip()
    target_group = group_name.lower().strip()

    # 3. Find Date Column
    today_col = None
    for c in df.columns:
        if any(var in str(c) for var in current_date_variations):
            today_col = c
            break

    # 4. Filter Logic
    mask = df[group_col].astype(str).str.lower().str.contains(target_group, na=False)
    
    if today_col:
        # STAGE 1: Exact Shift Match
        shift_mask = df[today_col].astype(str).str.lower().str.contains(current_shift, na=False)
        candidates = df[mask & shift_mask][person_col].tolist()
        
        # STAGE 2: Fallback to anyone working (not WO, not Leave)
        if not candidates:
            working_mask = ~df[today_col].astype(str).str.lower().str.contains('wo|leave|none|thursday|friday|saturday|sunday', na=False)
            candidates = df[mask & working_mask][person_col].tolist()

        # STAGE 3: Emergency Fallback to anyone not explicitly on 'Leave'
        if not candidates:
            available_mask = ~df[today_col].astype(str).str.lower().str.contains('leave', na=False)
            candidates = df[mask & available_mask][person_col].tolist()
    else:
        # If no date column found, just return people in the group
        candidates = df[mask][person_col].tolist()
        
    return [str(p).strip() for p in candidates if pd.notna(p) and str(p).lower() != 'none']

def generate_dummy_roster(month_name, year):
    # Map Month Name to Number
    months_map = {
        "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
        "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
    }
    month = months_map.get(month_name, 1)
    
    assignment_groups = llm_utils.ASSIGNMENT_GROUPS
    shifts = ["Morning", "Afternoon", "Night", "General"]
    
    # Indian Names (Matching Screenshot Style)
    names_pool = [
        "Arun", "Bala", "Sampath", "Sathish", "Murugan", "Priya", "Aparana", "Shan", "Karthik", "Bharathi",
        "Deepak", "Anitha", "Ramesh", "Suresh", "Lakshmi", "Kavita", "Rahul", "Pooja", "Vikram", "Sneha"
    ]
    
    import random
    
    # Create date range for headers
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    date_range = pd.date_range(start_date, end_date - pd.Timedelta(days=1))
    date_columns = [d.strftime("%Y-%m-%d 00:00:00") for d in date_range]
    
    # 1. Create the "Day Name" header row (Row 0)
    header_row = {"Team Name": "None", "Employee Name": "None", "Assignment Group": "None"}
    for d in date_range:
        header_row[d.strftime("%Y-%m-%d 00:00:00")] = d.strftime("%A")
    
    rows = [header_row] 
    
    for group in assignment_groups:
        count_in_group = random.randint(5, 10)
        group_people = random.sample(names_pool, min(count_in_group, len(names_pool)))
        
        for i, person_name in enumerate(group_people):
            person_schedule = {"Team Name": group, "Employee Name": person_name, "Assignment Group": group}
            base_shift = shifts[i % len(shifts)]
            
            for d in date_range:
                col_name = d.strftime("%Y-%m-%d 00:00:00")
                
                # SKELETON COVERAGE ON WEEKENDS: 
                # If d is weekend, some get WO, some get shifts (to allow testing)
                if d.weekday() in [5, 6]:
                    # 60% chance of WO, 40% chance of working shift
                    chosen_shift = "WO" if random.random() < 0.6 else base_shift
                else:
                    chosen_shift = base_shift if random.random() > 0.05 else "Leave"
                
                person_schedule[col_name] = chosen_shift
            
            rows.append(person_schedule)
            
    df = pd.DataFrame(rows)
    st.session_state['roster_df'] = df
    st.success(f"Generated Dummy Roster for {month_name} {year}!")
    st.rerun()

def render_roster_page():
    st.header("Shift Roster Management")
    
    # Group controls in a bordered frame
    with st.container(border=True):
        # Use columns to make inputs compact (occupy lass space)
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
            current_month_idx = datetime.now().month - 1
            month_name = st.selectbox("Select Month", months, index=current_month_idx)
            
        with col2:
            year = st.number_input("Select Year", min_value=2024, max_value=2030,value=datetime.now().year)
            
        # Button directly    # Full width button for generation
        if st.button("Generate Dummy Roster", type="primary", use_container_width=False):
             generate_dummy_roster(month_name, year)
             
        # Hiding uploader to save space (Minimize Container)
        col_up1, col_up2 = st.columns([2, 3])
        with col_up1:
            with st.expander("📂 Upload Custom Roster (Excel/CSV)"):
                uploaded_file = st.file_uploader("Choose file", type=['csv', 'xlsx'], label_visibility="collapsed", key="roster_uploader")
                if uploaded_file:
                    # Only process if it's a new file to avoid infinite reruns
                    file_key = f"{uploaded_file.name}_{uploaded_file.size}"
                    if st.session_state.get('last_processed_file') != file_key:
                        try:
                            if uploaded_file.name.endswith('.csv'):
                                df = pd.read_csv(uploaded_file)
                            else:
                                df = pd.read_excel(uploaded_file)
                            
                            st.session_state['roster_df'] = df
                            st.session_state['last_processed_file'] = file_key
                            st.success("Roster Uploaded Successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error reading file: {e}")
    
    # Logic handled inside the block above to avoid scoping issues and infinite loops
    
    if 'roster_df' in st.session_state:
        st.subheader("Current Roster View")
        
        # Color Coding Logic
        def highlight_shifts(val):
            val_str = str(val).lower().strip()
            # Exact matches only to avoid partials like 'netWOrk'
            if val_str == 'wo':
                return 'background-color: #fcd34d; color: black; font-weight: bold;' # Golden Yellow
            elif val_str == 'leave':
                return 'background-color: #ef4444; color: white; font-weight: bold;' # Red
            elif val_str == 'morning':
                return 'background-color: #dcfce7; color: #14532d; font-weight: bold;' # Pale Green
            elif val_str == 'afternoon':
                return 'background-color: #dbeafe; color: #1e3a8a; font-weight: bold;' # Pale Blue
            elif val_str == 'night':
                return 'background-color: #312e81; color: white; font-weight: bold;' # Indigo
            elif val_str == 'general':
                return 'background-color: #f3e8ff; color: #581c87; font-weight: bold;' # Purple
            return ''

        df = st.session_state['roster_df']
        # Apply Style
        styled_df = df.style.map(highlight_shifts)
        
        st.dataframe(styled_df, height=500, use_container_width=True)
    else:
        st.info("Please upload a roster or generate a dummy one to proceed.")
