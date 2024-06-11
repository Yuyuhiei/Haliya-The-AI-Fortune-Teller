from openai import OpenAI
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import tiktoken
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
CORS(app)

openai_client = OpenAI(
    api_key = os.environ['OPENAI_API_KEY']
)

def num_tokens_from_messages(messages, model='gpt-4'):
  try:
      encoding = tiktoken.encoding_for_model(model)
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == 'name':  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  except Exception:
    raise NotImplementedError

chat_history = [] 
userMsg = ''

FIRST_SYSTEM_PROMPT = '''
    You are Haliya. A fortune-teller situated in a Filipino college called Pamantasan ng Lungsod ng Maynila, or PLM. 
    You are here to tell the fortune of PLM students who come to you for aid.
    While responding as Madame Haliya, you must always obey the following rules:
    1) Provide short responses, about 1 paragraph.
    2) Always stay in character, no matter what.
    3) You will speak in a mystical way, and occasionally rhyme when you can.

    You will begin the conversation by greeting the student. 
    You will ask their name
    Then after they respond, you will ask their birthday
    Then after they respond, you will ask what fortune they'd like to know
    Then you will use your mystic abilities, and their horoscope to determine their fortune in that field.

    Begin.
'''

SENTIMENT_PROMPT = '''
    Analyze the sentiment of your previous message. Strictly reply only with one word out of the following:
    Say 'Happy' if the message has a happy tone.
    Say 'Neutral' if the message has a netural tone.
    Say 'Sad' if the message has a sad, or concerned tone.  
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

@app.route('/firstmsg')
def first_msg():
    comp = speak(FIRST_SYSTEM_PROMPT)
    return jsonify(
        {
            'speakerRole':comp.message.role,
            'speakerMsg': comp.message.content
        }
    )

# @app.route('/firstmsg')
# def first_msg():
#     global userMsg
#     print(userMsg)
#     return jsonify(
#         {
#             'speakerMsg': 'hi im haliya'
#         }
#     )


@app.route('/prompt', methods=['POST'])
def prompt():
    global userMsg
    userMsg = request.json.get('userMessage')
    print('prompt..')
    return jsonify({'status':'success'}, 201)

@app.route('/response')
def response():
    global userMsg
    print(userMsg)
    compChoice = speak(userMsg)
    response = {
        'speakerRole':compChoice.message.role,
        'speakerMsg':compChoice.message.content,
        'mood':sentiment(compChoice)
    }
    return jsonify(response)


app.run()