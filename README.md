# Voice AI Assistant

An intelligent AI chatbot with voice input and output capabilities, powered by Google Gemini and built with Streamlit. Experience natural conversations with AI through text or voice, with support for multiple languages and customizable AI personalities.

## Features

### Core Functionality
- 💬 **Interactive Chat Interface** - Beautiful Streamlit-based UI with persistent message history
- 🤖 **Google Gemini AI** - Powered by Gemini 2.0 Flash for intelligent, context-aware responses
- 🔄 **Streaming Responses** - Real-time response display for better user experience

### Voice Capabilities
- 🎤 **Voice Input** - Record your voice and have it converted to text automatically using Google Speech Recognition
- 🔊 **Text-to-Speech Output** - AI responses are automatically converted to audio using Google TTS (gtts)
- 🌍 **Multi-Language Support** - Voice recognition and TTS in 10+ languages:
  - English (US & UK)
  - Spanish
  - French
  - German
  - Chinese (Mandarin)
  - Japanese
  - Korean
  - Portuguese
  - Italian

### Advanced Features
- 🎭 **Multiple AI Personalities** - Choose between:
  - **General Assistant**: Helpful and knowledgeable for everyday tasks
  - **Study Buddy**: Patient and encouraging for learning and homework
  - **Gaming Helper**: Enthusiastic gaming expert for tips and strategies
- 🎯 **Voice Commands** - Control the app hands-free:
  - "Clear chat" or "Clear history" - Reset the conversation
  - "Change personality to Study Buddy" - Switch AI personalities
  - "Switch to Gaming Helper" - Change conversation style
- 🎨 **Modern UI** - Clean design with:
  - Visual activity indicators (🟢 Ready / 🔴 Listening)
  - Fixed bottom input for easy access
  - Mobile-responsive audio players
  - Organized sidebar with collapsible sections
- 💾 **Conversation Context** - Maintains full conversation history throughout the session

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core programming language |
| **Streamlit** | Web framework for the user interface |
| **Google Gemini API** | AI conversation model (gemini-2.0-flash) |
| **Google Speech Recognition** | Voice-to-text conversion |
| **Google Text-to-Speech (gtts)** | Text-to-audio conversion |
| **audio-recorder-streamlit** | Browser-based audio recording |
| **python-dotenv** | Environment variable management |

## Requirements

**Important:** This application requires **Python 3.9 or higher** to run properly.

The Google Gemini AI SDK (`google-generativeai`) is only compatible with Python 3.9+.

### Check Your Python Version

```bash
python --version
```

If you have Python 3.8 or lower, you'll need to upgrade Python to use this application.

### Dependencies

All required packages are listed in `requirements.txt`:

```
streamlit>=1.50.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
audio-recorder-streamlit>=0.0.8
SpeechRecognition>=3.10.0
gtts>=2.3.0
```

## Setup Instructions

### 1. Clone or Download the Repository

If you're using GitHub Classroom, clone your repository:

```bash
git clone <your-repository-url>
cd voice-ai-assistant
```

### 2. Install Python (if needed)

Download and install Python 3.9 or higher from [python.org](https://www.python.org/downloads/)

### 3. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Set Up Your API Key

1. Get a free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.env` file in the project directory (use `.env.example` as a template):

```bash
# Copy the example file
cp .env.example .env
```

3. Edit the `.env` file and add your API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**Important:** Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Usage

### Running the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

The app will automatically open in your default web browser at `http://localhost:8501`

### Using the Chat Interface

#### Text Input
- Type your message in the chat input box at the bottom
- Press Enter to send

#### Voice Input
1. Click the microphone button next to the chat input
2. Speak your message clearly
3. Wait for the speech recognition to process
4. Your message will be automatically sent to the AI

#### Listening to Responses
- Every AI response includes an audio player
- Click play to hear the response read aloud
- Audio is generated in the selected language

### Changing Settings

#### Select a Language
1. Open the sidebar (click the arrow in the top-left)
2. Expand "🎤 Voice Settings"
3. Choose your preferred language from the dropdown
4. Both voice input and audio output will use this language

#### Change AI Personality
1. Open the sidebar
2. Under "🎭 Personality", select from:
   - **General Assistant**: For general questions and tasks
   - **Study Buddy**: For learning and educational help
   - **Gaming Helper**: For gaming tips and discussions
3. Chat history will be cleared when you switch personalities

### Voice Commands

Control the app hands-free with these voice commands:

| Command | Action |
|---------|--------|
| "Clear chat" | Clears conversation history |
| "Clear history" | Clears conversation history |
| "Change personality to Study Buddy" | Switches to Study Buddy personality |
| "Switch to Gaming Helper" | Switches to Gaming Helper personality |
| "Change to General Assistant" | Switches to General Assistant personality |

**Note:** Voice commands work in any supported language!

### Visual Indicators

- 🟢 **Green Circle**: App is ready and waiting for input
- 🔴 **Red Circle**: App is listening or processing your voice input

## Project Structure

```
voice-ai-assistant/
├── app.py                 # Main application file with all functionality
├── requirements.txt       # Python package dependencies
├── .env                   # API key configuration (NOT tracked in git)
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore rules (protects .env)
└── README.md             # This documentation file
```

## Troubleshooting

### Installation Issues

**Error: No matching distribution found for google-generativeai**
- **Cause**: Python version is too old (below 3.9)
- **Solution**: Upgrade to Python 3.9 or higher from [python.org](https://www.python.org/downloads/)


### Runtime Issues

**Error: GEMINI_API_KEY not found**
- Make sure the `.env` file exists in the project root directory
- Verify the API key is correctly set in the `.env` file
- Check that the key format matches: `GEMINI_API_KEY=your_key_here`

**Voice input not working**
- Ensure your browser has microphone permissions enabled
- Check that your microphone is properly connected and working
- Try refreshing the browser page

**Speech recognition errors**
- Speak clearly and avoid background noise
- Ensure you have an active internet connection (Google Speech Recognition requires internet)
- Try selecting a different language in Voice Settings

**Audio not playing**
- Check your browser's audio settings
- Ensure audio is not muted
- Try a different browser (Chrome and Firefox work best)

**TTS audio in wrong language**
- Make sure you've selected the correct language in "🎤 Voice Settings"
- The TTS language automatically matches your voice input language setting

## License

This project is for educational purposes as part of a GitHub Classroom assignment.

## Author

Created as a GitHub Classroom assignment project.

---

**Powered by Google Gemini API**
