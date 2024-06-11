# IMPORTS ----------------------------------------
from openai import OpenAI
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import threading
import tiktoken
import os
from google.cloud import texttospeech
from playsound import playsound
from recorder import Recorder, WhisperTranscriber
from text_to_speech import GoogleCloudTextToSpeech # Add this line

# OPENAI SECTION ---------------------------------
app = Flask(__name__)
CORS(app)

openai_client = OpenAI(api_key = os.environ['OPENAI_API_KEY'])

def num_tokens_from_messages(messages, model='gpt-4'):
  try:
      encoding = tiktoken.encoding_for_model(model)
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == 'name':  # open('HaliyaCFG\life-path.txt, 'r')re's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  except Exception:
    raise NotImplementedError

chat_history = [] 
userMsg = ''
latestMsg = ''

# load category prompts
prompts = {}

f = open(os.getcwd()+r'\HaliyaCFG\life-path.txt', 'r')
prompts['life-path'] = f.read()
f = open(os.getcwd()+r'\HaliyaCFG\grades.txt', 'r')
prompts['grades'] = f.read()
f = open(os.getcwd()+r'\HaliyaCFG\health.txt', 'r')
prompts['health'] = f.read()
f = open(os.getcwd()+r'\HaliyaCFG\love.txt', 'r')
prompts['love'] = f.read()
f = open(os.getcwd()+r'\HaliyaCFG\decision.txt', 'r')
prompts['decision'] = f.read()
# load life-path prompt as default fallback
FIRST_SYSTEM_PROMPT = prompts['life-path']
currCategory = 'life-path'

SENTIMENT_PROMPT = '''
    Analyze the sentiment of your previous message. Strictly reply only with one word out of the following:
    Say 'Happy' if the message has a happy tone'/sentiment.
    Say 'Neutral' if the message has a netural tone/sentiment .
    Say 'Concerned' if the message has a sad, or concerned tone/sentiment.  
'''

def speak(msg):
    if not msg:
        return
    chat_history.append({'role':'user','content':msg})
    
    while (num_tokens_from_messages(chat_history) > 5000):
        chat_history.pop(1)
    completion = openai_client.chat.completions.create(
          model='gpt-3.5-turbo',
          messages=chat_history
        )
    chat_history.append({'role': completion.choices[0].message.role, 'content': completion.choices[0].message.content})
    
    output_path = r"tts-resources/output.mp3" # Path to save the output mp3 file
    tts.synthesize_speech(completion.choices[0].message.content, output_path)
    return completion.choices[0]

def sentiment(compChoice):
    msgs = []
    msgs.append({'role':compChoice.message.role, 'content':compChoice.message.content})
    msgs.append({'role':'user', 'content':SENTIMENT_PROMPT})
    completion = openai_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=msgs
    )
    return completion.choices[0].message.content

@app.route('/get-category')
def get_category():
    global currCategory
    return jsonify({'category':currCategory})

@app.route('/set-category', methods=['POST'])
def set_category():
    global FIRST_SYSTEM_PROMPT, currCategory
    promptChoice = request.json.get('category')
    currCategory = promptChoice
    FIRST_SYSTEM_PROMPT = prompts[promptChoice]
    print(FIRST_SYSTEM_PROMPT)
    clear_chat()
    return jsonify({'status':'success'}, 201)

@app.route('/clear-chat')
def clear_chat():
    chat_history.clear()
    return jsonify({'status':'success'})

@app.route('/firstmsg')
def first_msg():
    global latestMsg
    comp = speak(FIRST_SYSTEM_PROMPT)
    latestMsg = comp.message.content
    return jsonify(
        {
            'speakerRole':comp.message.role,
            'speakerMsg': comp.message.content
        }
    )

# @app.route('/firstmsg')
# def first_msg():
#     global userMsg, latestMsg
#     print(userMsg)
#     initial_message = 'hi im haliya'  
#     latestMsg = initial_message

#     return jsonify(
#             {
#                 'speakerMsg': initial_message
#             }
#         )
    

@app.route('/prompt', methods=['POST'])
def prompt():
    global userMsg
    userMsg = request.json.get('userMessage')
    print('prompt..')
    return jsonify({'status':'success'}, 201)

@app.route('/response')
def response():
    global userMsg, latestMsg
    print(userMsg)
    compChoice = speak(userMsg)
    latestMsg = compChoice.message.content
    response = {
        'speakerRole':compChoice.message.role,
        'speakerMsg':compChoice.message.content,
        'mood':sentiment(compChoice)
    }
    return jsonify(response)

# @app.route('/response')
# def response():
#     global latestMsg
#     temptxt = "maybe"
#     latestMsg = temptxt
#     return jsonify({'speakerMsg':temptxt, 'mood':'Concerned'})


# AUDIO PROCESSING SECTION------------------------
# initialize the TTS client
credentials_path = os.getcwd()+r"\tts-resources\GOOGLE-TTS-KEY.json" #replace with own tts key json
tts = GoogleCloudTextToSpeech(credentials_path)

@app.route('/speech')
def speech():
    global latestMsg
    output_path = os.getcwd()+r"\tts-resources\output.mp3"
    tts.synthesize_speech(latestMsg, output_path)
    tts.play_audio(output_path) 
    return jsonify({'status':'success'})

@app.route('/post-rasa', methods=['POST'])
def post_rasa():
    global latestMsg
    latestMsg = request.json.get('msg')
    print('rasa msg:', latestMsg)
    return jsonify({'status':'success'})

# Initialize global variables for the recorder and transcription
recorder = None
transcription_result = ""
WhisperAPIKey = os.environ['OPENAI_API_KEY']

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recorder
    recorder = Recorder()
    recording_thread = threading.Thread(target=recorder.start_recording)
    recording_thread.start()
    return jsonify({"status": "recording started"})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recorder, transcription_result
    recorder.stop_recording()
    whisper_transcriber = WhisperTranscriber(api_key=WhisperAPIKey)
    transcription_result = whisper_transcriber.transcribe(recorder.get_output_file())
    print("Transcription Result:", transcription_result)  # Print or use the transcript text
    return jsonify({"status": "recording stopped", "transcription": transcription_result})
# ------------------------------------------------
app.run()