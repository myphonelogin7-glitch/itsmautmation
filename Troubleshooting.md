# Troubleshooting Guide

## 1. Installation & Startup Issues

### "ModuleNotFoundError"
**Symptom**: App fails to start with `ModuleNotFoundError: No module named 'langchain'`.
**Solution**:
You are missing the required python libraries. Run the installation again:
```bash
pip install streamlit langchain-google-genai langchain fpdf watchdog python-dotenv
```

### "Streamlit is not recognized..."
**Symptom**: Command line says `streamlit` is not recognized.
**Solution**:
1.  Ensure Python is installed and added to your System PATH.
2.  Try running with python module syntax:
    ```bash
    python -m streamlit run app.py
    ```

## 2. AI & Functional Issues

### AI Responses are Generic / Mock Data shown
**Symptom**: The resolution steps say "Demo: AI Key missing" or generic steps without specific details.
**Cause**: The `GOOGLE_API_KEY` is missing or invalid.
**Solution**:
1.  Check if you set the environment variable.
2.  (For Development) Verify if the fallback key in `llm_utils.py` is valid or active.
3.  Check your Internet connection (required for Gemini API).

### "I'm currently offline (API Key Missing)"
**Symptom**: The chatbot replies with this exact error.
**Solution**: Same as above. The system cannot detect a valid API Key in `os.environ` or session state.

## 3. Dashboard / UI Issues

### No Audio / Voice Notification
**Symptom**: Toast says "Agent Tina is speaking", but no sound plays.
**Cause**: Browsers (Chrome/Edge) block "Autoplay" audio from websites that haven't had user interaction.
**Solution**:
1.  **Interact First**: Click anywhere on the dashboard before the timer hits 0.
2.  **Browser Settings**: Allow "Sound" for `localhost` in your browser settings.

### Timer is Frozen
**Symptom**: The "Next Run in..." timer stops counting.
**Solution**:
Refresh the browser tab (`Ctrl + R` or `F5`). This resets the session state and timer.

### "Login Failed" Loop
**Symptom**: You enter credentials but keep getting kicked back to login.
**Solution**:
1.  Ensure functionality of cookies in your browser.
2.  Use the hardcoded Admin credentials:
    *   User: `admin`
    *   Pass: `admin`
