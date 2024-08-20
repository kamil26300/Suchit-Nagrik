
# Suchit Nagrik

This project is a voice-activated assistant designed to provide information about government schemes in India. It uses speech recognition and natural language understanding to process user queries and retrieve relevant scheme details.


## API Reference

#### Get schemes by keywords

```http
  POST /schemes/data
```

| Body | Body Type     | Description | Response | Response Type |
| :-------- | :------- | :------------------------- | :--- | :-- |
| `Keywords[Tags, State]` | `object[Array, String]` | **Required**. Keywords | Schemes | `Array`

#### Get analytics

```http
  GET /schemes/analytics
```

| Response | Response Type     |
| :-------- | :------- |
| Category and their frequency      | `Object` | 


## Features

- Voice interaction: Users can interact with the assistant using their voice.
- Multiple languages: Supports Hindi, Tamil, Telugu, and English.
- Scheme information retrieval: Fetches details about various government schemes based on user queries.
- Natural language understanding: Extracts keywords and entities from user input to improve search accuracy.


## Installation

Clone the repository:
```bash
git clone https://github.com/kamil26300/Suchit-Nagrik
```

Install python packages:
```bash
// requirements.txt
deep_translator
dotenv
inflect
openai
requests
pyaudio
struct
pygame
wave
os
```
```bash
pip install -r requirements.txt   
```

Install ExpressJS dependencies:
```bash
// requirements.txt
cookie-parser
cors
dotenv
express
mongoose
morgan
nodemon
```
```bash
npm install -r requirements.txt   
```

Create a .env file in the project client directory and add the following environment variables:   
```bash
OPEN_AI_API_KEY = <your-openai-api-key>
MACHINE_LANGUAGE_CODE = <machine-language-code>
USER_LANGUAGE_CODE = <user-language-code>
MACHINE_LANGUAGE = <machine-language>
USER_LANGUAGE = <user-language>
OUTPUT_FILE = <path-to-output-audio-file>
INPUT_FILE = <path-to-input-audio-file>
BACK_END = <backend-server-url>
TTS_MODEL = <text-to-speech-model>
STT_MODEL = <speech-to-text-model>
GPT_TEXT_MODEL = <gpt-text-model>
```

## Deployment

Run the server:

```bash
  cd server
  npm run dev
```

Run python script:
```bash
  python SN.py
```



## Demo

    Hello from the pygame community. https://www.pygame.org/contribute.html
    SN: Hello, I'm here to help you with schemes. Select your language: Hindi, Tamil, Telugu, or English?

    * recording
    * done recording
    User: English

    SN: Hello. How can I help you with ?

    * recording
    * done recording
    User: handicraft societies in Puducherry.

    Keywords: {'tags': ['handicraft', 'society'], 'state': 'Puducherry'}
    SN: "Grant To Handicrafts Societies" Component of the "Development of Handicrafts" Scheme: “Grant To Handicrafts Societies” by the Department of Industries and Commerce, UT of Puducherry aims to encourage the creation 
    of Handicrafts Societies to enhance coordination and skill among craftspeople. Grants are provided to registered societies for organizing or participating in exhibitions.

    SN: Anything else ?

    * recording
    * done recording
    User: Good bye.

    SN: Good bye.



## Usage/Examples

Run the main.py script:
```bash
python main.py
```

The assistant will greet you and ask you to select your preferred language.

Once the language is selected, you can start asking questions about government schemes using your voice.

The assistant will process your query, retrieve relevant information from the backend server, and provide a spoken response.


## Tech Stack

**Server:** NodeJS, ExpressJS, python

**Database:** MongoDB

**AI:** openAI

**Translator:** deep_translator


## Authors

- [@kamil26300](https://www.github.com/kamil26300)
