# Haliya: AI Fortune Teller

Haliya is an AI Fortune Teller Bot integrated inside a website. It is especially designed for the students of PLM. Haliya offers six main features or categories; path, lovelife, grades, health, decision-maker, and prof-guesser (only PLM CS professors)


## Authors

- [@gekiiMei](https://github.com/gekiiMei)
- [@vinnyy](https://github.com/vinnyy-ph)
- [@alexong04](https://github.com/alexong04)
- [@bonitoflakes101](https://github.com/bonitoflakes101)





## Tech Stack

**Client:** React

**Server:** Node, Flask, Rasa

**Programming Languages:** JavaScript, Python

**Tools:** Figma, OpenAI API




## Features

- User-friendly UI and UX
- NLP (Both Filipino and English)
- Speech-recognition
- Emotion Changer (Haliya based on feedback)
- Generative AI (speech, natural language, and image)
- PLM scope learning


## Demo

**Main UI:**


https://github.com/Yuyuhiei/Haliya-The-AI-Fortune-Teller/assets/149577447/4ae055c4-f167-449f-af5b-fc2906eadbcb




















**Main feature (The main five categories):**


https://github.com/Yuyuhiei/Haliya-The-AI-Fortune-Teller/assets/149577447/110fc712-3bcc-4c62-8a4d-a78f1194cbf6




















**Prof-guesser:**


https://github.com/Yuyuhiei/Haliya-The-AI-Fortune-Teller/assets/149577447/86ad4d4b-a8e4-41a6-b72f-d62e154ac5ce




























## Screenshots
![main ui](https://github.com/Yuyuhiei/Haliya-The-AI-Fortune-Teller/assets/149577447/3b2f0138-81b9-4090-992e-ffde3b69a6c8)
![Main Chat](https://github.com/Yuyuhiei/Haliya-The-AI-Fortune-Teller/assets/149577447/2f8ea026-9ec2-41a1-8593-6407c30fb5ea)
![prof-guesser](https://github.com/Yuyuhiei/Haliya-The-AI-Fortune-Teller/assets/149577447/d3698558-f1b2-48d1-95c0-784de2879aaa)






# Setup
**Requirements**  
Python 3.10.11  
Node.js

**Step 1**  
Install Node.js & Python  
Clone repository

**Step 2**
cd into repository dir using CLI (Command Prompt, Powershell, etc.)  
![image](https://github.com/gekiiMei/ADET-AI-Exhibit/assets/86844554/7e230d5c-167f-48be-8667-55e93c74c05a)  
Create python virtual env by running `python -m venv .venv`  
cd into './.venv'  
`cd .venv`  
Run virtual env activation script `.\Scripts\activate`  

**NOTE:** Ensure that your IDE is using the virtual environment's (.venv) interpreter.  
&emsp;&ensp;in VS Code, this is done by running `>Python: Select Interpreter` in the command palette, and selecing the `.venv` environment.    

Install py backend reqs `pip install -r requirements.txt`

cd into './client'  
`cd client`  
run `npm install` to install react dependencies and reqs  

Train the RASA model by opening a terminal and cd-ing into `.venv/prof-guesser`, and running `rasa train`  


**Step 3**  
Host the frontend server by cd-ing back into the client folder, and running the command `npm run dev`.  
React frontend will now be hosted at localhost:5173;  
![image](https://github.com/gekiiMei/ADET-AI-Exhibit/assets/86844554/dab99563-6a07-4c45-af69-c0b30fc95f93)  

Host flask server by cd-ing back into the .venv folder, and running `python main.py` in the .venv terminal  

Host the RASA server by cd-ing into `.venv/prof-guesser`, and doing the following:  
Open a new terminal and cd into `.venv/prof-guesser`
run `rasa run actions`  
Open a new terminal and cd into `.venv/prof-guesser`  
run `rasa run --cors "*" --enable-api`  

Flask server will now be hosted at localhost:5000;
![image](https://github.com/gekiiMei/ADET-AI-Exhibit/assets/86844554/3c1b2d40-c359-426f-9ed9-0088a0eb697f)

# API Key config  
Add OpenAI API key as an Environment variable under `OPENAI_API_KEY`  
Python will access this value with `os.environ['OPENAI_API_KEY']`
