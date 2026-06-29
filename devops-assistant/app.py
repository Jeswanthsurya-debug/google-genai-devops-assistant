import streamlit as st
import google.generativeai as genai
import os

# Configure the Streamlit Page Layout
st.set_page_config(page_title="Gen AI DevOps Assistant", layout="wide")

# App Title & Branding
st.title("☁️ Google Cloud Gen AI DevOps Assistant")
st.subheader("Instant Build Log Parsing & Configuration Auto-Correction")
st.caption("Powered by Google Cloud Vertex AI & Gemini")

# Sidebar for API Configuration
with st.sidebar:
    st.header("Configuration")
    # Tries to get the key from environment variables first, otherwise asks user
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### Deployment Target")
    st.success("Target: Google Cloud Run (Serverless)")

# Main Layout: Split into Dual-Pane Interface
col1, col2 = st.columns(2)

with col1:
    st.header("📋 Input Workspace")
    st.write("Paste your broken shell scripts, YAML configurations, or raw terminal build logs below:")
    
    # Input box for logs/scripts
    user_input = st.text_area(
        "Logs / Code Input:", 
        placeholder="Example:\ndeploy.sh: line 14: [: ==: unary operator expected", 
        height=300
    )
    
    analyze_btn = st.button("🚀 Run Gemini Diagnostics", type="primary")

with col2:
    st.header("⚡ AI Response Panel")
    
    if analyze_btn:
        if not api_key:
            st.error("Please provide a valid Gemini API Key in the sidebar.")
        elif not user_input.strip():
            st.warning("Please paste some error logs or scripts to diagnose.")
        else:
            with st.spinner("Gemini is analyzing deployment context and rewriting code..."):
                try:
                    # Initialize the Gen AI SDK
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Construction of structured prompt engineering constraint
                    prompt = f"""
                    You are an expert DevOps engineer specializing in Google Cloud deployments, Docker, and CI/CD shell scripts.
                    Analyze the following error logs or configuration script. 
                    1. Identify the exact line and root cause of the error.
                    2. Provide a brief plain-English explanation.
                    3. Return the fully corrected configuration file or script inside a standard code block.
                    
                    User Input Payload:
                    {user_input}
                    """
                    
                    # Execute inference
                    response = model.generate_content(prompt)
                    
                    st.success("Diagnostics Complete!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred during processing: {str(e)}")
    else:
        st.info("Waiting for input workspace payload to trigger diagnosis...")
