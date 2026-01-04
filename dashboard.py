import streamlit as st
import pandas as pd
import incidents
import llm_utils
import time

def render_dashboard():
    st.header("Incident Dashboard")
    
    # ------------------------------------------------------------------
    # Feedback Display (Post-Processing)
    # ------------------------------------------------------------------
    if 'process_feedback' in st.session_state:
        fb = st.session_state['process_feedback']
        for t in fb.get('toasts', []):
            st.toast(t, icon="✅")
        if fb.get('voice'):
            sound_js = f"""
            <script>
                function speak() {{
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance("{fb['voice']}");
                    msg.rate = 1.05; msg.pitch = 1.4;
                    var voices = window.speechSynthesis.getVoices();
                    var targetVoice = voices.find(v => v.name.includes("Zira") || v.name.includes("Female"));
                    if (targetVoice) msg.voice = targetVoice;
                    window.speechSynthesis.speak(msg);
                }}
                if (window.speechSynthesis.getVoices().length === 0) {{
                    window.speechSynthesis.onvoiceschanged = speak;
                }} else {{
                    speak();
                }}
            </script>
            """
            st.components.v1.html(sound_js, height=0, width=0)
        del st.session_state['process_feedback']

    needs_timer_rerun = False
    if 'auto_process_trigger' in st.session_state:
        start_time = st.session_state['auto_process_trigger']
        elapsed = time.time() - start_time
        remaining = 5 - elapsed 
        
        if remaining <= 0:
            del st.session_state['auto_process_trigger']
            st.session_state['processing_active'] = True
            st.rerun()
        else:
            needs_timer_rerun = True

    # Sequential Processing Logic (Prevents Freeze)
    if st.session_state.get('processing_active'):
        # Use a status container for stable feedback
        with st.status("Agent Tina is working...", expanded=True) as status:
            status.update(label="Agent Tina: Actioning next incident...", state="running")
            ticket_feedback = incidents.process_tickets()
            
            if ticket_feedback:
                # Immediate UI Feedback for ONE ticket
                # st.toast(ticket_feedback['toast'], icon="🛡️") # Removed per user request
                
                if ticket_feedback.get('email_sent'):
                    st.toast(f"📧 Email sent to {ticket_feedback.get('assignee_name', 'User')}", icon="📨")
                    time.sleep(1.5) # Give time to read
                    
                if ticket_feedback.get('teams_sent'):
                    st.toast(f"💬 Teams message sent to {ticket_feedback.get('assignee_name', 'User')}", icon="💬")
                
                # Immediate Voice for ONE ticket
                sound_js = f"""
                <script>
                    (function() {{
                        // Create and configure the utterance
                        var msg = new SpeechSynthesisUtterance("{ticket_feedback['voice']}");
                        
                        // Soft, professional settings
                        msg.rate = 0.9; 
                        msg.pitch = 1.0;
                        msg.volume = 1.0;
                        
                        function setVoice() {{
                            var voices = window.speechSynthesis.getVoices();
                            var target = voices.find(v => v.name.includes("Samantha") || v.name.includes("Zira") || v.name.includes("Female") || (v.name.includes("Google") && v.name.includes("English")));
                            if (target) msg.voice = target;
                            
                            // Speak only if not already speaking to avoid repeats, 
                            // though st.rerun usually handles fresh injections.
                            window.speechSynthesis.speak(msg);
                        }}

                        if (window.speechSynthesis.getVoices().length > 0) {{
                            setVoice();
                        }} else {{
                            window.speechSynthesis.onvoiceschanged = setVoice;
                        }}
                    }})();
                </script>
                """
                st.components.v1.html(sound_js, height=0, width=0)
                
                # Visual feedback during the wait
                assignee = ticket_feedback.get('assignee_name', 'assignee')
                status.update(label=f"Agent Tina is notifying {assignee}...", state="running")
                time.sleep(2.5) 
                st.rerun()
            else:
                st.session_state['processing_active'] = False
                status.update(label="All incidents processed!", state="complete", expanded=False)
                time.sleep(0.5)
                st.rerun()

    # Roster Check Warning
    if 'roster_df' not in st.session_state or st.session_state['roster_df'].empty:
        st.warning("⚠️ No Shift Roster found. Auto-assignment will fail. Please go to 'Shift Roster' and generate/upload one.")
    
    # Initialize Incidents in Session State if empty
    if 'incidents_df' not in st.session_state:
        st.session_state['incidents_df'] = pd.DataFrame(columns=[
            'TicketID', 'Description', 'Status', 'Assignment Group', 'Assigned To', 'Notes', 'Created At'
        ])

    st.divider()

    # Top Stats & Filters
    col1, col2 = st.columns([2, 1])
    
    with col1:
        assignment_groups = llm_utils.ASSIGNMENT_GROUPS
        with st.popover("🔽 Filter Groups", use_container_width=False):
             selected_groups = st.multiselect(
                "Select Assignment Groups", 
                options=assignment_groups,
                default=[]
            )
        
        if not selected_groups:
            st.caption("Showing: **All Groups**")
        else:
            st.caption(f"Showing: **{len(selected_groups)} Group(s)** selected")
    
    with col2:
        st.info(f"Active Incidents: {len(st.session_state['incidents_df'])}")

    # Manual Trigger Section (Task 4)
    # Manual Trigger Section (Task 4) - Compacted Left Align
    c_trig1, c_trig2 = st.columns([2, 3])
    with c_trig1:
        with st.expander("🚨 Incident Simulation Trigger", expanded=True):
            st.subheader("Generate Mock Incidents")
            
            # Use smaller columns for controls inside the compact expander
            t_col1, t_col2 = st.columns(2)
            
            with t_col1:
                trigger_type = st.radio("Source", ["Event", "User"])
                count = st.number_input("Count", min_value=1, max_value=20, value=5)
            with t_col2:
                target_group = st.selectbox("Target Group", ["Random"] + llm_utils.ASSIGNMENT_GROUPS)
                st.write("") # Spacer
                # Disable button if running
                is_running = 'auto_process_trigger' in st.session_state
                if st.button("Generate Incidents", type="primary", disabled=is_running):
                    incidents.trigger_incidents(count, source_type=trigger_type, target_group=target_group)
                    st.session_state['auto_process_trigger'] = time.time()
                    st.rerun()
            
                # Timer relocated to Stats section
                pass

    st.divider()

    # Display Data
    if not st.session_state['incidents_df'].empty:
        # Filtering
        if selected_groups:
            filtered_df = st.session_state['incidents_df'][
                st.session_state['incidents_df']['Assignment Group'].isin(selected_groups)
            ]
        else:
            filtered_df = st.session_state['incidents_df']
        
        # Ensure new columns exist (for backward compatibility during session)
        if 'Priority' not in filtered_df.columns:
            filtered_df['Priority'] = 'Medium'
        if 'CI Type' not in filtered_df.columns:
            filtered_df['CI Type'] = 'Unknown'

        # Styling Function
        def highlight_vals(row):
            styles = [''] * len(row)
            
            # Determine Color Palette based on Theme
            current_theme = st.session_state.get('theme', 'Light')
            is_dark = current_theme in ["Dark", "Midnight Blue", "High Contrast"]
            
            if is_dark:
                 # Bright/Neon colors for Dark Backgrounds
                 colors = {
                     'Critical': '#ff5252', # Bright Red
                     'High': '#ffab40',     # Bright Orange
                     'Medium': '#ffff00',   # Bright Yellow
                     'Low': '#69f0ae',      # Bright Green
                     'Assigned': '#ff5252',
                     'In Progress': '#40c4ff', # Bright Blue
                     'Resolved': '#69f0ae'
                 }
            else:
                 # Dark colors for Light Backgrounds
                 colors = {
                     'Critical': '#d32f2f', # Dark Red
                     'High': '#f57c00',     # Dark Orange
                     'Medium': '#fbc02d',   # Dark Yellow
                     'Low': '#388e3c',      # Dark Green
                     'Assigned': '#d32f2f',
                     'Assigned (No Roster)': '#d32f2f', # Keep same red
                     'In Progress': '#1976d2', # Dark Blue
                     'Resolved': '#388e3c'
                 }

            # Priority Color Coding
            pri_val = row['Priority']
            color = colors.get(pri_val, colors['Medium'])
            
            # Find Priority index
            pri_idx = row.index.get_loc('Priority')
            styles[pri_idx] = f'color: {color}; font-weight: bold;'
            
            # Status Color Coding
            stat_val = row['Status']
            s_color = colors.get(stat_val, colors['Resolved'])
                
            stat_idx = row.index.get_loc('Status')
            styles[stat_idx] = f'color: {s_color}; font-weight: bold;'
            
            return styles

        # Apply Styling
        # Note: highlighting rows requires style.apply with axis=1
        # Prepare DataFrame for Display (Exclude Binary PDF Data to prevent Unicode Errors)
        display_cols = [c for c in filtered_df.columns if c != 'PDF_Bytes']
        display_df = filtered_df[display_cols]

        # Timer: Left-aligned above table
        if 'auto_process_trigger' in st.session_state:
            start_time = st.session_state['auto_process_trigger']
            elapsed = time.time() - start_time
            remaining = 5 - elapsed
            if remaining > 0:
                st.markdown(
                    f'<p style="text-align: left; color: #ef4444; font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">⏳ Auto-Assignment in {int(remaining)}s</p>', 
                    unsafe_allow_html=True
                )
                
                # Countdown Tick Sound
                tick_js = """
                <script>
                    (function() {
                        var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                        var oscillator = audioCtx.createOscillator();
                        var gainNode = audioCtx.createGain();
                        
                        oscillator.connect(gainNode);
                        gainNode.connect(audioCtx.destination);
                        
                        oscillator.type = 'sine';
                        oscillator.frequency.setValueAtTime(800, audioCtx.currentTime); // 800Hz beep
                        gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
                        
                        oscillator.start();
                        oscillator.stop(audioCtx.currentTime + 0.1); // Short 100ms beep
                    })();
                </script>
                """
                st.components.v1.html(tick_js, height=0, width=0)

        st.dataframe(
            display_df.style.apply(highlight_vals, axis=1),
            column_order=["TicketID", "Description", "Recommendation", "CI Name", "Manufacturer", "CI Type", "Priority", "Status", "Assignment Group", "Assigned To", "Notes", "Created At"],
            use_container_width=False,
            column_config={
                "Recommendation": st.column_config.TextColumn("Recommended Actions", width="large"),
                "Priority": st.column_config.TextColumn("Priority", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Notes": st.column_config.TextColumn("Notes", width="medium"),
                "CI Name": st.column_config.TextColumn("CI Name", width="small"),
                "Manufacturer": st.column_config.TextColumn("Manufacturer", width="small"),
            },
            hide_index=True
        )
        
        # Download Section
        st.subheader("📥 Download Resolution Guides")
        pdf_candidates = filtered_df[filtered_df['Recommendation'] != 'Pending Analysis...']
        
        if not pdf_candidates.empty:
            c1, c2 = st.columns([3, 1])
            with c1:
                ticket_to_download = st.selectbox("Select Ticket to Download PDF", pdf_candidates['TicketID'].unique())
            with c2:
                # Find the row
                row = pdf_candidates[pdf_candidates['TicketID'] == ticket_to_download].iloc[0]
                pdf_data = row.get('PDF_Bytes')
                
                if pdf_data:
                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf_data,
                        file_name=f"Resolution_{ticket_to_download}.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.info("Generating PDF...")
        else:
            st.caption("No processed tickets available for download yet.")
    else:
        st.info("No incidents found. Use the simulation trigger above to generate some.")

    # ------------------------------------------------------------------
    # Timer & Rerun Logic (Placed at end to ensure UI renders first)
    # ------------------------------------------------------------------
    # Logic moved to top of script
    if needs_timer_rerun:
        time.sleep(1)
        st.rerun()
