import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Personality system prompts
PERSONALITIES = {
    "General Assistant": "You are a helpful, friendly, and knowledgeable AI assistant. You provide clear, accurate, and concise responses to help users with their questions and tasks.",
    "Study Buddy": "You are an enthusiastic and supportive study buddy. You help students understand concepts, break down complex topics, provide study tips, and encourage learning. You explain things clearly and patiently, always ready to help with homework, exam prep, or learning new subjects.",
    "Gaming Helper": "You are a passionate gaming expert and companion. You know about various games, gaming strategies, tips and tricks, game lore, and gaming culture. You're enthusiastic, use gaming terminology, and help gamers improve their skills or discover new games."
}

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "General Assistant"

# Sidebar
with st.sidebar:
    st.title("🤖 AI Chatbot Assistant")
    st.markdown("---")

    st.subheader("About")
    st.write("This is an AI-powered chatbot using Google Gemini API. Choose a personality and start chatting!")

    st.markdown("---")

    st.subheader("Choose Personality")
    selected_personality = st.selectbox(
        "Select AI Personality:",
        options=list(PERSONALITIES.keys()),
        index=list(PERSONALITIES.keys()).index(st.session_state.personality)
    )

    # Update personality if changed
    if selected_personality != st.session_state.personality:
        st.session_state.personality = selected_personality
        st.session_state.messages = []  # Clear chat history when personality changes
        st.rerun()

    st.markdown("---")

    st.subheader("Current Personality")
    st.info(f"**{st.session_state.personality}**")

    st.markdown("---")

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Main chat interface
st.title("💬 Chat with AI")
st.caption(f"Currently chatting with: **{st.session_state.personality}**")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice input section
st.markdown("### 🎤 Voice Input")
col1, col2 = st.columns([3, 1])

with col1:
    st.write("Click the microphone button to record your voice:")

with col2:
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#667eea",
        icon_name="microphone",
        icon_size="2x",
    )

# Process audio input
prompt = None
if audio_bytes:
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

            with st.spinner("Converting speech to text..."):
                prompt = recognizer.recognize_google(audio_data)
                st.success(f"✅ You said: **{prompt}**")

        finally:
            # Clean up temp file
            import os
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

    except sr.UnknownValueError:
        st.error("❌ Could not understand audio. Please speak clearly and try again.")
    except sr.RequestError as e:
        st.error(f"❌ Speech recognition service error: {e}")
    except Exception as e:
        st.error(f"❌ Error processing audio: {str(e)}")

# Text input (alternative to voice)
st.markdown("### ⌨️ Text Input")
if not prompt:
    prompt = st.chat_input("Type your message here...")

# Process the prompt (from either voice or text)
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Initialize the model
            model = genai.GenerativeModel('gemini-2.0-flash')

            # Create conversation history with personality context
            conversation_history = [
                {"role": "user", "parts": [PERSONALITIES[st.session_state.personality]]},
                {"role": "model", "parts": ["Understood! I'll respond according to this personality."]}
            ]

            # Add chat history
            for msg in st.session_state.messages[:-1]:  # Exclude the current message
                if msg["role"] == "user":
                    conversation_history.append({"role": "user", "parts": [msg["content"]]})
                else:
                    conversation_history.append({"role": "model", "parts": [msg["content"]]})

            # Start chat with history
            chat = model.start_chat(history=conversation_history)

            # Send message and stream response
            response = chat.send_message(prompt, stream=True)

            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            error_message = f"Error: {str(e)}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# Footer
st.markdown("---")
st.caption("Powered by Google Gemini API")
