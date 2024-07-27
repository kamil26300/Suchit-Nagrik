from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from inflect import engine
from openai import OpenAI
import requests
import pyaudio
import struct
import pygame
import wave
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

machine_language_code = os.getenv("MACHINE_LANGUAGE_CODE")
user_language_code = os.getenv("USER_LANGUAGE_CODE")
machine_language = os.getenv("MACHINE_LANGUAGE")
user_language = os.getenv("USER_LANGUAGE")
output_file = os.getenv("OUTPUT_FILE")
input_file = os.getenv("INPUT_FILE")

def get_result_from_keywords(keywords):
	try:
		url = os.getenv("BACK_END") + "/schemes/data"
		response = requests.post(url, json=keywords)
		return response.json()
	except Exception as e:
		print(e)

def translate_text(text, src_lang, dest_lang):
	text = text or "No input. Try Again."
	translator = GoogleTranslator(source=src_lang, target=dest_lang)
	return translator.translate(text)

def TTS(translated_text):
	with client.audio.speech.with_streaming_response.create(
		model=os.getenv("TTS_MODEL"),
		voice="alloy",
		input=translated_text,
	) as response:
		response.stream_to_file(output_file)

def record_audio():
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	WAVE_OUTPUT_FILENAME = input_file
	THRESHOLD = 1000
	SILENCE_DURATION = 2

	p = pyaudio.PyAudio()

	stream = p.open(
		format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
	)

	print("* recording")

	frames = []
	silent_frames = 0

	while True:
		data = stream.read(CHUNK)
		frames.append(data)
		# Convert byte data to signed int
		decoded_data = struct.unpack(
				"<" + str(CHUNK) + "h", data
		)  # '<' for little-endian

		# Check for silence using the threshold
		if max(decoded_data) < THRESHOLD:
				silent_frames += 1
		else:
				silent_frames = 0

		if silent_frames >= SILENCE_DURATION * RATE / CHUNK:
				break  # Stop recording after silence duration
	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b"".join(frames))
	wf.close()

def STT(audio_file_path, user_language):
	with open(audio_file_path, "rb") as audio_file:
		transcript = client.audio.transcriptions.create(
			model=os.getenv("STT_MODEL"),
			file=audio_file,
			language=user_language
		)
	return transcript.text

def play_audio(audio_file):
	try:
		pygame.mixer.init()
		pygame.mixer.music.load(audio_file)
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy():
			pygame.time.Clock().tick(10)
	except pygame.error as e:
		print(f"Error playing audio: {e}")
	finally:
		pygame.mixer.music.stop()
		pygame.mixer.quit()

def extract_keywords(text):
	inflect_engine = engine()
	response = client.chat.completions.create(
		model=os.getenv("GPT_TEXT_MODEL"),  
    messages=[
			{"role": "system", "content": "You are an AI assistant designed to extract tags and states in India mentioned in the text provided."},
			{"role": "user", "content": f"Analyze this text and extract any tags and any state in India mentioned: Text: '{text}'"}
    ],
    functions=[
			{
				"name": "extract_tags_and_state",
				"description": "Extract relevant tags and the state from the text. Every tag should be a single word, if more split them into separate tags.",
				"parameters": {
					"type": "object",
					"properties": {
						"tags": {
							"type": "array",
							"items": {"type": "string"}
						},
						"state": {
							"type": "string",
							"description": "The state name mentioned in the text (if any)."
						}
					},
					"required": ["tags", "state"]
				}
			}
    ],
    function_call={"name": "extract_tags_and_state"}
	)
	result = eval(response.choices[0].message.function_call.arguments)
	
	unwanted_tags = {"scheme", "schemes", "Scheme", "Schemes"}
	result["tags"] = [tag for tag in result["tags"] if tag not in unwanted_tags]
	result["tags"] = [tag for tag in result["tags"] if tag != result["state"]]
	result["tags"] = [inflect_engine.singular_noun(tag) or tag for tag in result["tags"]]

	if len(result["tags"]) == 0:
		return "No tags mentioned"
	return result

def get_scheme_names(matches):
	text = ""
	for match in matches:
		text += f"{match["fields"]["schemeName"]}, "
	return text

def get_scheme_name_and_description(match):
	return f"{match["fields"]["schemeName"]}: {match["fields"]["briefDescription"]}"

def get_scheme(matches):
	if len(matches) == 0:
		return "No matches found. Try Again."
	elif len(matches) == 1:
		return get_scheme_name_and_description(matches[0])
	else:
		return get_scheme_names(matches)

def record_translate_text():
	record_audio()
	input = STT(input_file, user_language_code)
	if not input:
		record_translate_text()
		translate_text_play_audio("No Input. Try again.")
	else:
		translated_input = translate_text(input, user_language_code, machine_language_code) if (user_language_code != machine_language_code) else input
		print(f"User: {translated_input}\n")
		return translated_input

def translate_text_play_audio(text):
	print(f"SN: {text}\n")
	output = translate_text(text, machine_language_code, user_language_code) if (machine_language_code != user_language_code) else text
	TTS(output)
	play_audio(output_file)

def extract_keyword_and_get_scheme(text):
	output = extract_keywords(text)
	if isinstance(output, str):
		error_msg = f"{output}, please repeat."
		translate_text_play_audio(error_msg)
		record_translate_text()
	else:
		print(f"Keywords: {output}")
		matches = get_result_from_keywords(output)
		return get_scheme(matches)

def isFarewell(input_text):
	response = client.chat.completions.create(
    model=os.getenv("GPT_TEXT_MODEL"),
    messages=[
      {"role": "system", "content": "You will classify text as either 'farewell' or 'not_farewell'. Farewell should include 'bye', 'no, thanks' 'ok, bye', 'thank you' or words related to it."},
      {"role": "user", "content": input_text}
    ]
  )
	if response.choices[0].message.content.strip() == "farewell":
		translate_text_play_audio("Good bye.")
		exit()

def greeting_and_language_select():
	global user_language, user_language_code
	language_map = {
    "Hindi": "hi",
    "English": "en",
    "Telugu": "te",
    "Tamil": "ta"
  }
	greeting = "Hello, I'm here to help you with schemes. Select your language: Hindi, Tamil, Telugu, or English?"
	translate_text_play_audio(greeting)
	
	while True:
		language = record_translate_text().capitalize().replace(".", "")
		if language in language_map:
			user_language = language
			user_language_code = language_map[language]
			break
		else:
			error_message = "Invalid language selection. Please choose from: Hindi, Tamil, Telugu, or English."
			translate_text_play_audio(error_message)

def elseQuery():
	translate_text_play_audio("Anything else ?")
	
def openingQuery():
	translate_text_play_audio("Hello. How can I help you with ?")

def test():
	greeting_and_language_select()
	# English
	openingQuery()
	while True:
		input = record_translate_text()
		# input = Handicrafts Socities in puducherry
		isFarewell(input)
		output = extract_keyword_and_get_scheme(input)
		translate_text_play_audio(output)
		elseQuery()

test()