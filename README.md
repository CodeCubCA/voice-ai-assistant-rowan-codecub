# Voice AI Assistant

An AI-powered chatbot application using Streamlit and Google Gemini API.

## Features

- 💬 **Interactive Chat Interface** - Beautiful Streamlit-based UI with message history
- 🎭 **Multiple Personalities** - Choose between General Assistant, Study Buddy, or Gaming Helper
- 🎤 **Voice Input** - Record your voice and have it converted to text automatically
- 🌍 **Multi-Language Support** - Voice recognition in 10+ languages (English, Spanish, French, German, Chinese, Japanese, Korean, Portuguese, Italian, and more)
- 🎯 **Voice Commands** - Control the app with voice commands like "clear chat" or "change personality to Study Buddy"
- 🔄 **Streaming Responses** - Real-time response display for better user experience
- 💾 **Conversation History** - Maintains context throughout the conversation
- 🎨 **Modern UI** - Clean and intuitive design with visual activity indicators

## Requirements

**Important:** This application requires **Python 3.9 or higher** to run properly.

The Google Gemini AI SDK (`google-generativeai`) is only compatible with Python 3.9+.

### Check Your Python Version

```bash
python --version
```

If you have Python 3.6 or lower, you'll need to upgrade Python to use this application.

## Installation

1. **Upgrade Python** (if needed)
   - Download Python 3.11+ from [python.org](https://www.python.org/downloads/)

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Key**
   - Your Gemini API key is already configured in the `.env` file
   - If you need to change it, edit the `.env` file

## Usage

Run the application:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

### Using Voice Input

1. Click the microphone button next to the chat input
2. Speak your message clearly
3. The app will automatically convert your speech to text
4. Select your preferred language from the sidebar for better accuracy

### Voice Commands

You can control the app using voice commands:

- **Clear chat**: Say "clear chat" or "clear history" to reset the conversation
- **Change personality**: Say "change personality to Study Buddy", "switch to Gaming Helper", or "change to General Assistant"

These commands work in any supported language!

## Personalities

### General Assistant
A helpful, friendly, and knowledgeable AI assistant that provides clear and accurate responses.

### Study Buddy
An enthusiastic study partner that helps with understanding concepts, homework, and exam preparation.

### Gaming Helper
A passionate gaming expert who knows about games, strategies, tips, tricks, and gaming culture.

## Technology Stack

- **Frontend:** Streamlit
- **AI Model:** Google Gemini 2.0 Flash
- **Language:** Python 3.9+
- **Environment:** python-dotenv for configuration

## Project Structure

```
voice-ai-assistant/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # API key configuration (not tracked in git)
├── .env.example          # Template for API key
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Troubleshooting

**Error: No matching distribution found for google-generativeai**
- This means your Python version is too old (below 3.9)
- Solution: Upgrade to Python 3.9 or higher

**Error: GEMINI_API_KEY not found**
- Make sure the `.env` file exists in the project directory
- Verify the API key is correctly set in the `.env` file

## License

This project is for educational purposes.

## Author

Created as a GitHub Classroom assignment project.
