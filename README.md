SUCHIT NAGRIK
This project is a voice-activated assistant designed to provide information about government schemes in India. It uses speech recognition and natural language understanding to process user queries and retrieve relevant scheme details.

Features
Voice interaction: Users can interact with the assistant using their voice.
Multiple languages: Supports Hindi, Tamil, Telugu, and English.
Scheme information retrieval: Fetches details about various government schemes based on user queries.
Natural language understanding: Extracts keywords and entities from user input to improve search accuracy.
Dependencies
OpenAI: Used for speech-to-text, text-to-speech, and natural language processing.
Deep Translator: Handles language translation.
PyAudio: Records audio input from the microphone.
Pygame: Plays audio output.
Requests: Makes API calls to the backend server for scheme data.
Inflect: Handles word pluralization and singularization.
Wave: Processes audio files.
Python-dotenv: Loads environment variables from a .env file.


**Installation**
    Clone the repository:
        Bash
            git clone <repository-url>
    
    Install dependencies:
        Bash
            pip install -r requirements.txt   
    
    Create a .env file in the project root directory and add the following environment variables:   
        OPEN_AI_API_KEY=<your-openai-api-key>
        MACHINE_LANGUAGE_CODE=<machine-language-code> # e.g., 'en'
        USER_LANGUAGE_CODE=<user-language-code> # e.g., 'hi'
        MACHINE_LANGUAGE=<machine-language> # e.g., 'English'
        USER_LANGUAGE=<user-language> # e.g., 'Hindi'
        OUTPUT_FILE=<path-to-output-audio-file> # e.g., 'output.mp3'
        INPUT_FILE=<path-to-input-audio-file> # e.g., 'input.wav'
        BACK_END=<backend-server-url> # URL of the backend server providing scheme data
        TTS_MODEL=<text-to-speech-model> # e.g., 'tts-1'
        STT_MODEL=<speech-to-text-model> # e.g., 'whisper-1'
        GPT_TEXT_MODEL=<gpt-text-model> # e.g., 'gpt-3.5-turbo-16k'


Usage
    Run the main.py script:
        Bash
            python main.py
    
    The assistant will greet you and ask you to select your preferred language.
    Once the language is selected, you can start asking questions about government schemes using your voice.
    The assistant will process your query, retrieve relevant information from the backend server, and provide a spoken response.


**Sample Usage**

![image](https://github.com/user-attachments/assets/77046830-f836-43c1-bc11-3668eb826e8b)
![image](https://github.com/user-attachments/assets/ffc2e0ef-c462-4229-b4fb-1abd1212dd90)
