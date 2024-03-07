from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import UserProfile
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse, HttpResponse
import os
import speech_recognition as sr
from django.conf import settings
from gtts import gTTS
import io
import pyttsx3


def index(request):
    return render(request, 'index2.html')

@api_view(['POST'])
def authenticate_generateToken(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        print('user: ', user)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_user(request):
    try:
        print('request data: ', request.data)
        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid():
            user = userSerializer.save()
            profileFields = {
                'user': user.id,
                'fullname': request.data.get('fullname'),
                'sex': request.data.get('sex'),
                'phone_no': request.data.get('phone_no'),
                'country': request.data.get('country')
            }
            profileSerializer = UserProfileSerializer(data=profileFields)
            if profileSerializer.is_valid():
                profileSerializer.save()
                return Response(profileSerializer.data, status=status.HTTP_201_CREATED)
            else:
                user.delete()
                return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(profileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def convert_speech_to_text(request):
    # Path to the speech file inside your Django app directory
    # speech_file_path = os.path.join(os.path.dirname(__file__), 'path', 'to', 'your', 'speech.wav')
    # speech_file_path = os.path.join(settings.MEDIA_ROOT, 'speech_to_text', 'userprofile', 'speech1.wav')

    # speech_file_path = 'speech_to_text/userprofile/speech1.wav'
    speech_file_path = os.path.join(settings.BASE_DIR, 'userprofile', 'speech1.wav')

    recognizer = sr.Recognizer()

    with sr.AudioFile(speech_file_path) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            print('recognize text: ', text)
            return JsonResponse({'text': text})
        except sr.UnknownValueError:
            return JsonResponse({'error': 'Speech could not be understood'})
        except sr.RequestError as e:
            return JsonResponse({'error': f"Could not request results from Google Speech Recognition service: {e}"})

@api_view(['POST'])
def convert_speech_to_text2(request):
    print('convert_speech_to_text2')
    audio_file = request.FILES.get('audio_file')
    # audio_file = os.path.join(settings.BASE_DIR, 'userprofile', 'speech1.wav')

    print("audio_file: ", audio_file)
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Read the audio file
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

        # Convert speech to text
        try:
            text = recognizer.recognize_google(audio_data)
            print('recognize text: ', text)
            return JsonResponse({'text': text})
        except sr.UnknownValueError:
            return JsonResponse({'error': 'Speech could not be understood'})
        except sr.RequestError as e:
            return JsonResponse({'error': f"Could not request results from Google Speech Recognition service: {e}"})
        

@api_view(['POST'])
def welcome_message(request):
    text = request.data.get('text', '')
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return JsonResponse({'message': 'Text spoken successfully'})

