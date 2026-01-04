import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import time
from datetime import datetime
import roster
import llm_utils

def generate_realistic_scenario(group):
    scenarios = {
        "Windows": [("Blue Screen of Death (BSOD) reported", "Server"), ("Active Directory Login Failure", "Service"), ("Print Spooler Service Stuck", "Service"), ("C: Drive Disk Space Low", "Server")],
        "Unix": [("Kernel Panic on Production Node", "Server"), ("SSH Daemon failed to start", "Service"), ("Inode usage 100% on /var", "Server"), ("Zombie processes count high", "Server")],
        "Storage": [("SAN Multipath Flapping", "Hardware"), ("NAS Volume Read-Only", "Hardware"), ("LUN Latency High > 20ms", "Hardware"), ("RAID Battery Failure Warning", "Hardware")],
        "Backup": [("NetBackup Job Failed: Error 96", "Service"), ("Tape Library Robot Arm Stuck", "Hardware"), ("Snapshot Deletion Failed", "Service"), ("Retention Policy not Applied", "Service")],
        "Network": [("Switch Port Flapping", "Network Device"), ("Packet Loss on Uplink", "Network Device"), ("VPN Tunnel Down", "Service"), ("BGP Neighborship Down", "Network Device")],
        "Firewall": [("Palo Alto HA Sync Down", "Network Device"), ("Rule 45 blocking valid traffic", "Configuration"), ("VPN User Unable to Connect", "Service"), ("Firewall Throughput Spiking", "Network Device")],
        "Tools": [("JIRA Slow Response Time", "Application"), ("GitLab Runner Offline", "Application"), ("Jenkins Build Queue Stuck", "Application"), ("ServiceNow API Timeout", "Application")],
        "Database": [("Oracle Tablespace Full", "Database"), ("SQL Server Deadlock Detected", "Database"), ("MySQL Replication Lag High", "Database"), ("Postgres Connection Pool Exhausted", "Database")],
        "Cloud": [("AWS EC2 Instance Status Check Failed", "Cloud Resource"), ("Azure VM Allocation Failed", "Cloud Resource"), ("S3 Bucket Access Denied", "Cloud Resource"), ("Kubernetes Pod Loop Crash", "Cloud Resource")]
    }
    
    defaults = [("General System Error", "Server"), ("Performance Degradation", "Application")]
    options = scenarios.get(group, defaults)
    return random.choice(options)

def trigger_incidents(count, source_type="Event", target_group="Random"):
    
    assignment_groups = llm_utils.ASSIGNMENT_GROUPS
    
    # Detailed Manufacturer Mapping (User Provided)
    # Mapping: Group -> Category (CI Type) -> [Manufacturers]
    manufacturer_mapping = {
        'Windows': {
            'Server': ['Dell', 'HPE', 'Lenovo', 'Fujitsu', 'Cisco'],
            'Virtualization': ['VMware', 'Microsoft', 'Citrix', 'Red Hat', 'Nutanix'],
            'Service': ['Microsoft'] # Fallback
        },
        'Unix': {
            'Server': ['IBM', 'Oracle', 'HPE', 'Dell', 'Fujitsu'],
            'UNIX Platforms': ['Oracle', 'IBM', 'HPE', 'Hitachi', 'Bull']
        },
        'Storage': {
            'Hardware': ['NetApp', 'Dell EMC', 'HPE', 'IBM', 'Hitachi Vantara'], # SAN/NAS
            'Object Storage': ['Pure Storage', 'Scality', 'MinIO', 'Cloudian', 'Huawei']
        },
        'Backup': {
            'Hardware': ['Dell EMC', 'HPE', 'IBM', 'Quantum', 'ExaGrid'], # Appliances
            'Service': ['Veritas', 'Veeam', 'Commvault', 'Rubrik', 'Cohesity'] # Software
        },
        'Network': {
            'Network Device': ['Cisco', 'Juniper', 'Arista', 'HPE Aruba', 'Extreme Networks'], # Switching
            'Routing': ['Cisco', 'Juniper', 'Nokia', 'Huawei', 'MikroTik']
        },
        'Firewall': {
            'Network Device': ['Palo Alto Networks', 'Fortinet', 'Check Point', 'Cisco', 'Sophos'], # Appliances
            'Configuration': ['Palo Alto Networks', 'Fortinet'],
            'Service': ['Zscaler', 'Akamai', 'Cloudflare', 'Forcepoint', 'McAfee'] # Secure Access
        },
        'Database': {
            'Database': ['Oracle', 'Microsoft', 'IBM', 'SAP', 'MongoDB'], # Platforms
            'Hardware': ['Oracle', 'Dell', 'HPE', 'IBM', 'Fujitsu'] # DB Hardware
        },
        'Tools': {
            'Application': ['SolarWinds', 'Dynatrace', 'Datadog', 'Nagios', 'Zabbix'], # Monitoring
            'Automation': ['ServiceNow', 'BMC', 'Ansible', 'Terraform', 'Puppet']
        },
        'Cloud': {
            'Cloud Resource': ['AWS', 'Microsoft Azure', 'Google Cloud', 'Oracle Cloud', 'IBM Cloud'], # Providers
            'Hardware': ['Dell', 'HPE', 'Cisco', 'Supermicro', 'Lenovo']
        }
    }
    
    priorities = ['Critical', 'High', 'Medium', 'Low']
    
    new_incidents = []
    
    for _ in range(count):
        # 1. Determine Group
        if target_group and target_group != "Random":
            group = target_group
        else:
            group = random.choice(assignment_groups)
            
        # 2. Get Attributes
        desc, ci_type = generate_realistic_scenario(group)
        priority = random.choice(priorities)
        
        # Add Prefix
        if source_type == "Event":
             desc = f"[Alert] {desc}"
        else:
             desc = f"User Reported: {desc}"
             
        # 3. Generate CI Name & Manufacturer
        # Get specific manufacturer list for this Group and CI Type
        group_map = manufacturer_mapping.get(group, {})
        # Try exact match, then 'Server' or 'Hardware' fallbacks, then generic
        mfg_list = group_map.get(ci_type)
        if not mfg_list:
            # Fallback logic if specific CI Type key isn't found
            if 'Server' in group_map: mfg_list = group_map['Server']
            elif 'Hardware' in group_map: mfg_list = group_map['Hardware']
            else: mfg_list = ['Generic', 'Unknown']
            
        manufacturer = random.choice(mfg_list)
        
        # Random CI Name
        alphanum = ''.join(random.choices('0123456789', k=3))
        # Handle case where ci_type might be shorter than 3 chars (unlikely but safe)
        ci_prefix = ci_type[:3].lower() if len(ci_type) >=3 else ci_type.lower()
        ci_name = f"{ci_prefix}-{manufacturer[:3].lower()}-{alphanum}".upper()
        
        new_incidents.append({
            'TicketID': f"INC{random.randint(10000, 99999)}",
            'Description': desc,
            'CI Type': ci_type,
            'CI Name': ci_name,
            'Manufacturer': manufacturer,
            'Priority': priority,
            'Status': 'Assigned',
            'Assignment Group': group,
            'Assigned To': 'Unassigned',
            'Notes': '',
            'Recommendation': 'Pending Analysis...',
            'Created At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    

    
    new_df = pd.DataFrame(new_incidents)
    
    if 'incidents_df' in st.session_state:
        # Ensure new columns exist in old dataframe if it exists
        if 'Priority' not in st.session_state['incidents_df'].columns:
             st.session_state['incidents_df']['Priority'] = "Medium"
        if 'CI Type' not in st.session_state['incidents_df'].columns:
             st.session_state['incidents_df']['CI Type'] = "Unknown"
             
        st.session_state['incidents_df'] = pd.concat([st.session_state['incidents_df'], new_df], ignore_index=True)
    else:
        st.session_state['incidents_df'] = new_df
        
    st.success(f"Generated {count} new incidents from {source_type} targeting {target_group}!")
    
    # Simulate the "Wait 2 minutes" requirement immediately after generation for the flow
    # In a real app, this would be asynchronous. Here we block or create a "Process" step.
    # The requirement says "Once generated wait 2 minutes", then check.
    # We will implement this in the process_tickets function as a visual delay.

def process_tickets():
    """
    Processes ONE ticket and returns feedback for that specific ticket.
    """
    if 'incidents_df' not in st.session_state or st.session_state['incidents_df'].empty:
        return None

    df = st.session_state['incidents_df'].copy()
    df['Status'] = df['Status'].astype(str).str.strip()
    to_process = df[df['Status'] == 'Assigned']
    
    if to_process.empty:
        return None

    # Process exactly ONE incident
    index = to_process.index[0]
    row = to_process.iloc[0]
    ticket_id = row['TicketID']
    
    group = row['Assignment Group']
    candidates = roster.get_personnel_for_group(group)
    manufacturer = row.get('Manufacturer', 'Generic')
    ci_type = row.get('CI Type', 'Unknown')
    
    feedback = {"toast": "", "voice": "", "ticket_id": ticket_id}

    if candidates:
        if 'rr_state' not in st.session_state:
            st.session_state['rr_state'] = {}
        current_rr_index = st.session_state['rr_state'].get(group, -1)
        next_rr_index = (current_rr_index + 1) % len(candidates)
        assignee = candidates[next_rr_index]
        st.session_state['rr_state'][group] = next_rr_index
        
        status_val = 'In Progress'
        recommendation = llm_utils.generate_resolution_steps(row['Description'], group, manufacturer, ci_type)
        llm_note = llm_utils.generate_acknowledgment_note(row['Description'], group)
        
        feedback["toast"] = f"✅ {ticket_id} Assigned to {assignee}"
        feedback["voice"] = f"Hi {assignee}, a new incident has been assigned to your name. Kindly check and take action. Thank you!"
        feedback["email_sent"] = True
        feedback["teams_sent"] = True
        
        # Simulated Notifications (MOCK)
        # In real app: call email_api.send(...) and teams_api.post(...)
        notif_status = "[Email & Teams Sent]"
    else:
        assignee = "Unassigned"
        status_val = 'Assigned (No Roster)' 
        timestamp = datetime.now().strftime("%H:%M")
        shift_now = roster.determine_current_shift()
        st.warning(f"Ticket {ticket_id}: No personnel found for '{group}' on '{shift_now}' shift.")
        recommendation = f"ACTION REQUIRED: No personnel found for group '{group}' during '{shift_now}' shift. \n\nPlease update the Shift Roster for today's date."
        llm_note = f"System could not auto-assign. Verified no '{shift_now}' shift members."
        feedback["toast"] = f"⚠️ {ticket_id} Assignment Failed"
        notif_status = "[No Personnel - Roster Alert]"

    # Pass the resolved assignee name back
    feedback['assignee_name'] = assignee

    # Update Dataframe Fields
    df.at[index, 'Status'] = status_val
    df.at[index, 'Assigned To'] = assignee
    df.at[index, 'Recommendation'] = recommendation
    
    # Cumulative Notes (ALIGNED WITH SCREENSHOT)
    current_notes = str(df.at[index, 'Notes']) if pd.notna(df.at[index, 'Notes']) else ""
    timestamp = datetime.now().strftime("%H:%M")
    
    if candidates:
        notification_note = f"[{timestamp}] SYSTEM: Ticket assigned to {assignee} {notif_status}."
    else:
        notification_note = f"[{timestamp}] SYSTEM: Assignment failed (No '{roster.determine_current_shift()}' shift staff)."
        
    new_note_entry = f"[{timestamp}] Agent Tina: {llm_note}\n{notification_note}".strip()
    df.at[index, 'Notes'] = (current_notes + "\n" + new_note_entry).strip()
    
    # PDF
    pdf_bytes = llm_utils.create_pdf_recommendation(ticket_id, row['Description'], recommendation, manufacturer)
    df.at[index, 'PDF_Bytes'] = pdf_bytes
    
    # Store results
    st.session_state['incidents_df'] = df
    return feedback
