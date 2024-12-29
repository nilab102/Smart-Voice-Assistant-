import os
import datetime
import streamlit as st
from groq import Groq
from audio_recorder_streamlit import audio_recorder
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

prompt_details = """
The AI will only ask for the fields that are specifically mentioned by the user. The AI should understand and infer the necessary details from natural language inputs.

Workflow Details:
1. The AI analyzes the user's query to identify the task type (e.g., reconciliation request).
2. It checks if all **required fields** for the identified task are provided.
3. If any field is missing, the AI will prompt the user to fill in the missing information:
   - The prompt should be natural and conversational. Example: "Can you provide the project name or ID for this request?"
4. Once all the required fields are provided, the AI will summarize the input and confirm:
   "Are you sure you want to proceed?"
5. If the user confirms, the AI adds the request to the database.
6. If any required fields remain unfilled, the AI will continue to prompt until all necessary details are gathered.

Supported Tasks and Required Fields:
1. **Reconciliation Request**
   - **Required Fields:**
     - Project/Product name or ID
     - Price
     - Reason

   **Example Interaction:**
   User: "I need to request money for project X to buy tools. Amount: X Riyals."
   AI Workflow:
   - Analyzes the user's input and identifies the missing fields.
   - If the price is mentioned, but other fields are missing, the AI asks: "Can you please provide the reason for this request?"
   - Once all fields are provided, the AI will display the summary:
     "Project: X, Price: Y Riyals, Reason: Buy tools. Are you sure you want to proceed?"
   - The user confirms, and the AI processes the request.

"""


# Initialize session state for LLM
if "llm" not in st.session_state:
    st.session_state["llm"] = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        temperature=0.3,
        model_name="llama3-8b-8192"
    )

# Initialize session state for conversation buffer
if "conversation_buf" not in st.session_state:
    st.session_state["conversation_buf"] = ConversationChain(
        llm=st.session_state["llm"],
        memory=ConversationBufferMemory()
    )

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Initialize session state for audio
if "last_audio" not in st.session_state:
    st.session_state["last_audio"] = None

# Save context to the memory object
if "initialized_memory" not in st.session_state:
    st.session_state["conversation_buf"].memory.save_context( # changed line
        {"user_input": "Add task handling details"},
        {"ai_output": prompt_details}
    )
    st.session_state["initialized_memory"] = True

# Function to save audio file
def save_audio_file(audio_bytes):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.wav"
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name

# Function to transcribe audio file using Groq
def transcribe_audio(file_path):
    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(file_path, file.read()),
            model="whisper-large-v3",
            language="en",
            response_format="verbose_json",
        )
        return transcription.text

# Main Streamlit App
def main():
    st.title("Smart Voice Assistant")
    st.markdown(
        """
        Welcome to your personal assistant! You can interact with the AI by typing your input or using your voice. 
        Use the tabs below to switch between text and voice input modes.
        """
    )

    # Tabs for input modes
    tab1, tab2 = st.tabs(["🖊️ Text Input", "🎤 Voice Input"])

    with tab1:
        st.subheader("Text Input")
        st.write("Type your input below and press Send to interact with the AI.")
        
        with st.form("text_input_form"):
            user_input = st.text_area("Enter your text input:", "", height=100)
            submit_button = st.form_submit_button("Send")

        if submit_button and user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})

            with st.spinner("Generating AI response..."):
                ai_response = st.session_state["conversation_buf"].run(user_input)

            st.session_state["messages"].append({"role": "ai", "content": ai_response})
            st.markdown(f"**AI:** {ai_response}")

    with tab2:
        st.subheader("Voice Input")
        st.write("Record your voice below and let the AI respond.")

        # Reset audio state when switching to the Voice Input tab
        if st.session_state.get("last_tab") != "voice":
            st.session_state["last_audio"] = None  # Clear previous audio state
            st.session_state["last_tab"] = "voice"

        # Record new audio
        audio_bytes = audio_recorder()

        if audio_bytes:
            # Save and process only new audio
            if st.session_state["last_audio"] != audio_bytes:
                st.session_state["last_audio"] = audio_bytes  # Save the current audio
                st.audio(audio_bytes, format="audio/wav")
                file_path = save_audio_file(audio_bytes)
                st.success(f"Audio saved as {file_path}")

                with st.spinner("Processing transcription..."):
                    transcript = transcribe_audio(file_path)

                st.markdown(f"**Transcription:** {transcript}")

                st.session_state["messages"].append({"role": "user", "content": transcript})

                with st.spinner("Generating AI response..."):
                    ai_response = st.session_state["conversation_buf"].run(transcript)

                st.session_state["messages"].append({"role": "ai", "content": ai_response})
                st.markdown(f"**AI:** {ai_response}")

    # Display conversation history
    st.divider()
    st.subheader("Conversation History")
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**AI:** {message['content']}")

if __name__ == "__main__":
    main()
