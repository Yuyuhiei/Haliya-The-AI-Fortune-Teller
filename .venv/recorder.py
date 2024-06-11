from pvrecorder import PvRecorder
import wave
import struct
import threading
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
sys_device_index = 0 #set index here

# PASET NALANG RIN NG DEVICE_INDEX DITO, akin kasi 1 eh, paconfigure nalang hardware. Use XIAN's version of recorder.py

class Recorder:
    global sys_device_index
    def __init__(self, device_index=sys_device_index, output_file='user_voice_record.wav', frame_length=512, channels=1, sampwidth=2, framerate=16000):
        self.device_index = device_index
        self.output_file = output_file
        self.frame_length = frame_length
        self.channels = channels
        self.sampwidth = sampwidth
        self.framerate = framerate
        self.recorder = None
        self.wave_file = None
        self.stop_event = threading.Event()
        self.recording_thread = None

    def list_devices(self):
        devices = PvRecorder.get_available_devices()
        for index, device in enumerate(devices):
            print(f"[{index}] {device}")

    def start_recording(self):
        self.recorder = PvRecorder(device_index=self.device_index, frame_length=self.frame_length)
        self.recorder.start()
        print("Recording...")

        self.wave_file = wave.open(self.output_file, 'w')
        self.wave_file.setnchannels(self.channels)
        self.wave_file.setsampwidth(self.sampwidth)
        self.wave_file.setframerate(self.framerate)

        self.recording_thread = threading.Thread(target=self._write_frames)
        self.recording_thread.start()

    def stop_recording(self):
        self.stop_event.set()
        self.recording_thread.join()
        self.recorder.stop()
        self.wave_file.close()
        print("Recording stopped.")

    def _write_frames(self):
        try:
            while not self.stop_event.is_set():
                frame = self.recorder.read()
                self.wave_file.writeframes(struct.pack('h' * len(frame), *frame))
        finally:
            self.recorder.stop()
            self.wave_file.close()

    def get_output_file(self):
        return self.output_file


class WhisperTranscriber:
    def __init__(self, api_key, model_id='whisper-1'):
        self.client = OpenAI(api_key=api_key)
        self.model_id = model_id

    def transcribe(self, audio_file_path, language='en'):
        with open(audio_file_path, 'rb') as audio_file:
            response = self.client.audio.transcriptions.create(
                model=self.model_id,
                file=audio_file,
                language=language
            )
            if response and hasattr(response, 'text'):
                return response.text
            else:
                return "Transcription failed or returned empty text."


