from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserProfileSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.http import JsonResponse
import speech_recognition as sr
import pyttsx3

def index(request):
    return render(request, 'index.html')

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
    
@api_view(['POST'])
def convert_speech_to_text2(request):
    # audio_file = os.path.join(settings.BASE_DIR, 'userprofile', 'speech1.wav')
    audio_file = request.FILES.get('audio_file')

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            return JsonResponse({'text': text})
        except sr.UnknownValueError:
            return JsonResponse({'error': 'Speech could not be understood'})
        except sr.RequestError as e:
            return JsonResponse({'error': f"Could not recognize speech: {e}"})
        
@api_view(['POST'])
def welcome_message(request):
    text = request.data.get('text', '')
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return JsonResponse({'message': 'Mwssage spoken successfully'})

