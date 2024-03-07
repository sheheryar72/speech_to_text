from django.urls import path
from .views import add_user, authenticate_generateToken, index, convert_speech_to_text, convert_speech_to_text2, welcome_message
# from .consumers import SpeechToTextConsumer

urlpatterns = [
    path('authenticate/', authenticate_generateToken, name='authenticate_generateToken'),
    path('add/', add_user, name='add_user'),
    path('index/', index, name='index'),
    path('convert/', convert_speech_to_text, name='convert_speech_to_text'),
    path('convert2/', convert_speech_to_text2, name='convert_speech_to_text2'),
    path('welcome_message/', welcome_message, name='speak_text'),
]


