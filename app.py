import streamlit as st
import os
import tempfile
from src.analyzer import ScreenAnalyzer

# --- Page Configuration ---
st.set_page_config(
    page_title="AI QA Analyst",
    page_icon="vodafone_icon.png",  # Updated to use local asset if possible, or emoji fallback
    layout="wide",
    initial_sidebar_state="expanded"
)

import base64

# --- Load Custom CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Try to load the CSS file
try:
    load_css("src/styles.css")
except FileNotFoundError:
    st.warning("src/styles.css not found. Some styles may be missing.")

# --- Header with Logo ---
try:
    img_base64 = get_img_as_base64("vodafone_icon.png")
    header_html = f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{img_base64}" class="logo-img">
        <div>
            <h1>AI QA Analyst & Automation Generator</h1>
            <p style="margin: 0; color: #555;">Vodafone Intelligent Automation</p>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading logo: {e}")
    st.title("AI QA Analyst & Automation Generator")



st.markdown("""
<div style="background-color: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;">
    Autonomously analyzes screen recordings, extracts <b>Test Scenarios</b>, and generates <b>Maestro</b> automation scripts.
</div>
""", unsafe_allow_html=True)

# st.divider() removed in favor of card spacing

# --- Sidebar (Configuration) ---
with st.sidebar:
    st.image("vodafone_icon.png", width=50)
    st.header("⚙️ Configuration")

    # API Key Management
    env_api_key = os.getenv("GOOGLE_API_KEY")
    api_key_input = st.text_input(
        "Google API Key",
        value=env_api_key if env_api_key else "",
        type="password",
        help="API Key from Google AI Studio."
    )

    st.markdown("""
    <div style="background-color: #ffe6e6; padding: 15px; border-radius: 8px; border-left: 4px solid #e60000; color: #333;">
    <b>How it Works:</b>
    <ol style="margin-left: -15px;">
        <li>Upload video</li>
        <li>AI analyzes frames</li>
        <li>Generates QA Report & Code</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

# --- Main Flow ---
st.markdown("### 📤 Upload Recording")
uploaded_file = st.file_uploader("Drop screen recording here (.mp4, .mov)", type=['mp4', 'mov', 'avi'])

if uploaded_file:
    # 1. Save Video Temporarily
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    # 2. Two Column Layout (Video and Action)
    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        st.subheader("📹 Source Video")
        st.video(uploaded_file)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("🧠 Intelligence Engine")
        
        # Using a container for better spacing
        with st.container():
            st.write("Ready to analyze operational flow.")
            analyze_btn = st.button("Start Analysis ►", type="primary", use_container_width=True)

        if analyze_btn:
            if not api_key_input:
                st.error("Please provide Google API Key first!")
            else:
                status_box = st.status("Initializing AI Agents...", expanded=True)

                try:
                    # Call Backend
                    analyzer = ScreenAnalyzer(api_key=api_key_input)

                    status_box.write("📤 Uploading text/video to Gemini 2.5 Flash...")
                    status_box.write("👁️ Computer Vision analysis in progress...")
                    status_box.write("✍️ Writing test scenarios...")

                    # Analyze
                    result = analyzer.analyze_video(video_path)

                    status_box.update(label="Analysis Complete!", state="complete", expanded=False)

                    # --- SHOW RESULTS (Tabs) ---
                    st.markdown("### 📊 Results")
                    tab1, tab2 = st.tabs(["📝 Manual Test Report", "🤖 Maestro Script"])

                    with tab1:
                        st.success("Generated Manual QA Report")
                        st.markdown(result.get("human_readable_report", "No report generated."))

                    with tab2:
                        st.info("Mobile.dev Maestro Automation Yaml")
                        yaml_code = result.get("maestro_yaml", "# No code generated")
                        st.code(yaml_code, language='yaml')

                        st.download_button(
                            label="📥 Download flow.yaml",
                            data=yaml_code,
                            file_name="flow.yaml",
                            mime="text/yaml"
                        )

                except Exception as e:
                    status_box.update(label="Analysis Failed", state="error")
                    st.error(f"Error Details: {str(e)}")

                finally:
                    # Cleanup
                    if os.path.exists(video_path):
                        os.remove(video_path)