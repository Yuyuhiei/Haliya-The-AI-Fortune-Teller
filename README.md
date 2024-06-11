# Project Haliya

# SETUP
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
