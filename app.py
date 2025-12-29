import streamlit as st
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
from gtts import gTTS

# Load environment variables
load_dotenv()

# Get HuggingFace API token
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Initialize HuggingFace Inference Client
client = InferenceClient(token=HUGGINGFACE_TOKEN)

# Model selection for HuggingFace
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"

# Personality system prompts
PERSONALITIES = {
    "General Assistant": "You are a helpful, friendly, and knowledgeable AI assistant. You provide clear, accurate, and concise responses to help users with their questions and tasks. IMPORTANT: When responding in any language other than English, respond ONLY in that language without adding pinyin, romanization, or translations. Just use the native script naturally.",
    "Study Buddy": "You are an enthusiastic and supportive study buddy. You help students understand concepts, break down complex topics, provide study tips, and encourage learning. You explain things clearly and patiently, always ready to help with homework, exam prep, or learning new subjects. IMPORTANT: When responding in any language other than English, respond ONLY in that language without adding pinyin, romanization, or translations. Just use the native script naturally.",
    "Gaming Helper": "You are a passionate gaming expert and companion. You know about various games, gaming strategies, tips and tricks, game lore, and gaming culture. You're enthusiastic, use gaming terminology, and help gamers improve their skills or discover new games. IMPORTANT: When responding in any language other than English, respond ONLY in that language without adding pinyin, romanization, or translations. Just use the native script naturally."
}

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for improved UI
st.markdown("""
<style>
    /* Fix the chat input at the bottom */
    .stChatFloatingInputContainer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #0e1117;
        padding: 1rem;
        z-index: 999;
        border-top: 1px solid #262730;
    }

    /* Add padding to main content to prevent overlap */
    .main .block-container {
        padding-bottom: 120px;
    }

    /* Ensure chat messages scroll properly */
    section[data-testid="stChatMessageContainer"] {
        margin-bottom: 100px;
    }

    /* Make audio players full-width on mobile */
    @media (max-width: 768px) {
        .stAudio {
            width: 100% !important;
        }
    }

    /* Improve spacing for audio sections */
    .stAudio {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "General Assistant"

if "language" not in st.session_state:
    st.session_state.language = "en-US"

if "is_speaking" not in st.session_state:
    st.session_state.is_speaking = False

if "last_audio_bytes" not in st.session_state:
    st.session_state.last_audio_bytes = None

if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = {}

if "processing" not in st.session_state:
    st.session_state.processing = False

# TTS audio generation function
def generate_tts_audio(text, message_index, show_feedback=True):
    """Generate TTS audio for a message and store it in session state"""
    if message_index not in st.session_state.tts_audio:
        # Warn for very long messages
        if len(text) > 500 and show_feedback:
            st.warning("⏳ Long message - audio generation may take a moment...")

        # Clean and prepare text for TTS
        # Remove markdown formatting and special characters that might cause issues
        import re
        tts_text = text.replace("**", "").replace("*", "").replace("_", "")
        tts_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', tts_text)  # Remove markdown links
        tts_text = re.sub(r'`([^`]+)`', r'\1', tts_text)  # Remove code formatting

        # Truncate extremely long messages for TTS
        tts_text = tts_text[:1000] + "..." if len(tts_text) > 1000 else tts_text

        try:
            # Convert language code from recognition format to TTS format
            # Map speech recognition codes (en-US, es-ES) to gTTS codes (en, es)
            lang_map = {
                "en-US": "en",
                "en-GB": "en",
                "es-ES": "es",
                "fr-FR": "fr",
                "de-DE": "de",
                "zh-CN": "zh-CN",
                "ja-JP": "ja",
                "ko-KR": "ko",
                "pt-PT": "pt",
                "it-IT": "it"
            }

            # Get TTS language code from current session language
            tts_lang = lang_map.get(st.session_state.language, "en")

            # Create TTS object with selected language
            tts = gTTS(text=tts_text, lang=tts_lang, slow=False)

            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            # Store in session state
            st.session_state.tts_audio[message_index] = audio_buffer.read()

            return st.session_state.tts_audio[message_index]
        except Exception as e:
            if show_feedback:
                st.error(f"❌ Audio generation failed: {str(e)}")
            return None

    return st.session_state.tts_audio.get(message_index)

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot Assistant")
    st.markdown("---")

    # About section in expander
    with st.expander("ℹ️ About", expanded=False):
        st.write("AI-powered chatbot using HuggingFace API with voice input/output capabilities.")
        st.write("**Features:** Voice chat, TTS audio, multiple personalities, and multi-language support.")
        st.write(f"**Model:** {MODEL_NAME}")

    st.markdown("---")

    # Personality Selection
    st.subheader("🎭 Personality")
    selected_personality = st.selectbox(
        "Choose AI personality:",
        options=list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.personality),
        help="Select how the AI should respond to you"
    )

    # Update personality if changed
    if selected_personality != st.session_state.personality:
        st.session_state.personality = selected_personality
        st.session_state.messages = []  # Clear chat history when personality changes
        st.rerun()

    st.info(f"**Active:** {st.session_state.personality}")

    st.markdown("---")

    # Voice Settings in expander
    with st.expander("🎤 Voice Settings", expanded=False):
        st.subheader("🌍 Language")
        languages = {
            "English (US)": "en-US",
            "English (UK)": "en-GB",
            "Spanish": "es-ES",
            "French": "fr-FR",
            "German": "de-DE",
            "Chinese (Mandarin)": "zh-CN",
            "Japanese": "ja-JP",
            "Korean": "ko-KR",
            "Portuguese": "pt-PT",
            "Italian": "it-IT"
        }

        selected_language = st.selectbox(
            "Voice language:",
            options=list(languages.keys()),
            index=list(languages.values()).index(st.session_state.language),
            help="Select language for both voice input and audio output"
        )

        new_language = languages[selected_language]
        if new_language != st.session_state.language:
            st.session_state.language = new_language
            st.success(f"🌍 Changed to {selected_language}")

    # Voice Commands Help
    with st.expander("🎙️ Voice Commands", expanded=False):
        st.markdown("""
        **Available voice commands:**

        🗑️ **Clear chat:**
        - "clear chat" or "clear history"

        🎭 **Change personality:**
        - "Change personality to Study Buddy"
        - "Switch to Gaming Helper"
        - "Change to General Assistant"

        💡 **Tips:**
        - Speak clearly and naturally
        - Commands work in any language
        - Use voice settings for better accuracy
        """)

    st.markdown("---")

    if st.button("🗑️ Clear Chat History", help="Remove all messages and start fresh"):
        st.session_state.messages = []
        st.session_state.tts_audio = {}  # Clear audio cache
        st.rerun()

# Main chat interface
st.title("💬 Chat with AI")
st.caption(f"Currently chatting with: **{st.session_state.personality}**")

# Show helpful tips if no messages yet
if len(st.session_state.messages) == 0:
    st.info("""
    👋 **Welcome! Here's how to use the voice chat:**
    - 🎤 **Voice Input**: Click the microphone button to speak
    - ⌨️ **Text Input**: Type your message in the text box
    - 🔊 **Audio Output**: Listen to AI responses with built-in audio players
    - 🎭 **Personalities**: Change AI personality from the sidebar
    - 🌍 **Languages**: Voice recognition supports 10+ languages
    """)

# Display chat messages with TTS audio players
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    # Add audio player for assistant messages (outside chat_message)
    if message["role"] == "assistant":
        audio_data = generate_tts_audio(message["content"], idx, show_feedback=False)
        if audio_data:
            # Add visual separator
            st.markdown("---")

            # Use columns for better layout
            col_audio, col_spacer = st.columns([5, 1])
            with col_audio:
                st.markdown("🔊 **Listen to response:**")
                st.audio(audio_data, format='audio/mp3')

            # Add spacing after audio
            st.markdown("")

# Visual status indicator
status_col1, status_col2 = st.columns([1, 5])
with status_col1:
    if st.session_state.is_speaking:
        st.markdown("### 🔴")
    else:
        st.markdown("### 🟢")

with status_col2:
    if st.session_state.is_speaking:
        st.warning("🎤 Listening / Processing...")
    else:
        st.success("✅ Ready - Click microphone to speak")

# Chat input area - text input (must be outside columns for Streamlit compatibility)
text_prompt = st.chat_input("Type your message or use the microphone...")

# Voice input option
st.markdown("---")
st.markdown("**Or use voice input:**")
audio_bytes = audio_recorder(
    text="",
    recording_color="#e74c3c",
    neutral_color="#667eea",
    icon_name="microphone",
    icon_size="2x",
    key="audio_recorder"
)

# Process audio input
prompt = None
if audio_bytes and audio_bytes != st.session_state.last_audio_bytes:
    # Store this audio to prevent reprocessing
    st.session_state.last_audio_bytes = audio_bytes

    # Set speaking state
    st.session_state.is_speaking = True

    try:
        # The audio_recorder returns WebM audio, we need to save it directly
        import tempfile

        # Save audio bytes to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name

        # Convert to WAV using pydub if needed, or try direct recognition
        try:
            # Try to use speech recognition directly on the audio
            recognizer = sr.Recognizer()

            # Try to load as WAV first
            try:
                with sr.AudioFile(tmp_file_path) as source:
                    # Adjust for ambient noise
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)
            except:
                # If that fails, the audio is likely WebM format
                # We need to convert it to WAV first
                from pydub import AudioSegment
                import os

                # Load WebM and convert to WAV
                audio = AudioSegment.from_file(tmp_file_path, format="webm")
                wav_path = tmp_file_path.replace(".webm", ".wav")
                audio.export(wav_path, format="wav")

                # Now use the WAV file
                with sr.AudioFile(wav_path) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio_data = recognizer.record(source)

                # Clean up WAV file
                os.unlink(wav_path)

            with st.spinner("🎤 Converting speech to text..."):
                # Use selected language for recognition
                prompt = recognizer.recognize_google(audio_data, language=st.session_state.language)
                st.success(f"✅ You said: **{prompt}**")

                # Check for voice commands
                prompt_lower = prompt.lower()

                # Clear chat command
                if "clear chat" in prompt_lower or "clear history" in prompt_lower:
                    st.session_state.messages = []
                    st.session_state.is_speaking = False
                    st.success("🗑️ Chat history cleared by voice command!")
                    st.rerun()

                # Personality change commands
                for personality in PERSONALITIES.keys():
                    personality_lower = personality.lower()
                    if (f"change personality to {personality_lower}" in prompt_lower or
                        f"switch to {personality_lower}" in prompt_lower or
                        f"change to {personality_lower}" in prompt_lower):
                        st.session_state.personality = personality
                        st.session_state.messages = []
                        st.session_state.is_speaking = False
                        st.success(f"🎭 Switched to {personality} by voice command!")
                        st.rerun()

                # Clear speaking state for normal messages after processing
                st.session_state.is_speaking = False

        finally:
            # Clean up temp file
            import os
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

    except sr.UnknownValueError:
        st.session_state.is_speaking = False
        st.error("❌ Could not understand audio. Please speak clearly and try again.")
    except sr.RequestError as e:
        st.session_state.is_speaking = False
        st.error(f"❌ Speech recognition service error: {e}")
    except Exception as e:
        st.session_state.is_speaking = False
        st.error(f"❌ Error processing audio: {str(e)}")
else:
    # Reset speaking state when no audio
    st.session_state.is_speaking = False

# Use text input if no voice input
if not prompt and text_prompt:
    prompt = text_prompt
    # Reset speaking state when using text input
    st.session_state.is_speaking = False

# Process the prompt (from either voice or text)
if prompt and not st.session_state.processing:
    # Set processing flag to prevent duplicate processing
    st.session_state.processing = True

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Build conversation history with personality context
            messages = [
                {"role": "system", "content": PERSONALITIES[st.session_state.personality]}
            ]

            # Add chat history
            for msg in st.session_state.messages[:-1]:  # Exclude the current message
                messages.append({"role": msg["role"], "content": msg["content"]})

            # Add current user message
            messages.append({"role": "user", "content": prompt})

            # Call HuggingFace API
            with st.spinner("🤔 Thinking..."):
                response = client.chat_completion(
                    messages=messages,
                    model=MODEL_NAME,
                    max_tokens=500,
                    stream=False
                )

                # Extract the response content
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    full_response = response.choices[0].message.content
                else:
                    full_response = "Sorry, I couldn't generate a response."

            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

            # Generate TTS audio for the new response with visual feedback
            message_index = len(st.session_state.messages) - 1
            with st.spinner("🎵 Generating audio..."):
                generate_tts_audio(full_response, message_index)

            # Clear processing flag and rerun to display audio player
            st.session_state.processing = False
            st.rerun()

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            error_message = f"Error: {str(e)}\n\n```\n{error_details}\n```\n\nPlease make sure your HUGGINGFACE_TOKEN is set correctly in the .env file."
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.session_state.processing = False

# Footer
st.markdown("---")
st.caption("Powered by HuggingFace API")
