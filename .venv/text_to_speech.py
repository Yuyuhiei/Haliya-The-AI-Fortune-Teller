from google.cloud import texttospeech
from playsound import playsound
import os

class GoogleCloudTextToSpeech:
    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        print(self.credentials_path)
        self.client = texttospeech.TextToSpeechClient()

    # transforms given text input from AI to MP3 file
    def synthesize_speech(self, text_to_speak, output_path):
        input_text = texttospeech.SynthesisInput(text=text_to_speak)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Studio-O",
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1
        )

        response = self.client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "{output_path}"')

    # this just plays that MP3 file
    def play_audio(self, output_path):
        print('playing mp3: '+output_path)
        playsound(output_path)
        os.remove(output_path)
        print('deleted previous mp3')