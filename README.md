# Smart Voice Assistant

This is a Streamlit-based Smart Voice Assistant application that allows users to interact with an AI using text or voice inputs. The AI processes user queries using Groq's APIs and LangChain's memory tools.

## Features
- **Text and Voice Input**:
  - Type messages or record your voice to interact with the AI.
- **Task Handling**:
  - AI can handle specific workflows, such as reconciliation requests, by gathering required fields interactively.
- **LangChain Integration**:
  - Maintains context across multi-turn conversations with `ConversationChain` and `ConversationBufferMemory`.
- **Audio Transcription**:
  - Supports audio transcription using the Whisper API.

## How to Run

### Prerequisites
- Python 3.10 or higher

### Setting Up the Environment
1. **Create a Virtual Environment**:
   Run the following command to create a virtual environment for your project:
   ```bash
   python -m venv venv
2. **Activate the Virtual Environment**:

    On Windows:
    ```bash
    venv\Scripts\activate
    ```

    On Mac/Linux:
    ```bash
    source venv/bin/activate
    ```

3. **Install Dependencies**:
    Install all the required libraries using the `requirements.txt` file:
    ```bash
    pip install -r requirment.txt
    ```

4. **Set Up the .env File**:
    Create a `.env` file in the root directory of your project and add your Groq API key:
    ```env
    GROQ_API_KEY=your_groq_api_key
    ```

5. **Run the App**:
    Start the Streamlit app:
    ```bash
    streamlit run app.py
    ```
