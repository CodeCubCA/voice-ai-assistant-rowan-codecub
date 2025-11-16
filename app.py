import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

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

# Chat input
if prompt := st.chat_input("Type your message here..."):
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
