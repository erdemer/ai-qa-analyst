# 🕵️‍♂️ AI QA Analyst & Automation Generator

**Vodafone Intelligent Automation**

This tool autonomously analyzes screen recording videos, extracts business logic and **Test Scenarios**, and automatically generates **Maestro** automation scripts. It empowers QA teams to move from manual testing to automated verification with the power of multimodal AI.

![Vodafone Material Theme UI](vodafone_icon.png)

## 🚀 Key Features

- **Video-to-Code**: Upload a screen recording (`.mp4`, `.mov`) of your app flow.
- **Multimodal Analysis**: Uses **Google Gemini 1.5 Pro/Flash** to understand visual elements and user interactions.
- **Auto-Generated Scenarios**: Produces a detailed, step-by-step manual test report.
- **Maestro Automation**: Generates ready-to-run `flow.yaml` scripts for [mobile.dev Maestro](https://maestro.mobile.dev/).
- **Vodafone Material Design**: A premium, branded UI with smooth animations and intuitive layout.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Core**: Google Gemini API (via `google-generativeai`)
- **Styling**: Custom CSS with Material Design principles & Vodafone Branding

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-qa-analyst
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Ensure you have `streamlit` and `google-generativeai` installed.*

4. **Set up API Key**
   You can provide your Google Gemini API key nicely in the UI sidebar, or set it as an environment variable:
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

## ▶️ Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

1. Open the local URL (usually `http://localhost:8501`).
2. Enter your **Google API Key** in the sidebar (if not set in env).
3. **Drag & Drop** a screen recording video into the upload area.
4. Click **Start Analysis**.
5. Wait for the AI to process the video.
6. View the **Test Scenarios** in the first tab and download the **Maestro Code** from the second tab.

## 📂 Project Structure

```
├── app.py              # Main Streamlit application entry point
├── src/
│   ├── analyzer.py     # AI Logic & Gemini API integration
│   └── styles.css      # Custom Vodafone Material Theme styles
├── requirements.txt    # Python dependencies
├── vodafone_icon.png   # Branding asset
└── README.md           # Project documentation
```
