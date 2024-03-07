# consumers.py

from channels.generic.websocket import WebsocketConsumer
import speech_recognition as sr

class SpeechToTextConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        r = sr.Recognizer()
        with sr.AudioFile(text_data) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            self.send(text)
