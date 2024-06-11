note:
- not fully functional yet
- somehow, calling utterance from actions.py is not working, will debug more

how to run in terminal:
1. make sure prof-guesser folder is in same location w/ .venv folder
2. set terminal path to path of prof-guesser folder
3. enter "rasa train"
4. open another terminal w/ the same path
5. in that terminal, enter "rasa run actions"
6. switch back to orig terminal, and enter "rasa shell"

how to use bot:
- enter "start" for bot to start asking y/n questions
- can use arrow keys to select choices

how to train bot in terminal:
- follow same steps in "how to run in terminal", however in step 6, instead of entering "rasa shell", enter "rasa interactive" instead
- this would be similar to running the bot on terminal, however, every step and bot response is validated and can be corrected