from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.timezone import now, localtime
from .models import EmotionEntry, Profile, EmotionRecording, Feedback
from .forms import (SignUpForm, EmotionEntryForm, FeedbackForm,
                    EmotionRecordingForm, VideoUploadForm)
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
import requests
import speech_recognition as sr
from collections import Counter
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from django.views.decorators.csrf import csrf_exempt




def get_previous_emotion(user):
    try:
        last_entry = EmotionEntry.objects.filter(user=user).latest('created_at')
        return last_entry.emotion_level
    except EmotionEntry.DoesNotExist:
        return "No hay entradas anteriores."

def analyze_emotion(description):
    url = 'https://fd1f-167-0-128-69.ngrok-free.app/analisis?text='
    response = requests.get(url + description)
    
    if response.status_code == 200:
        data = response.json()
        emotion = data.get('emotion')
        return emotion
    else:
        return None
    
@login_required
def emotion_entry(request):
    if request.method == 'POST':
        form = EmotionEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.emotion_type = analyze_emotion(entry.description)
            entry.save()
            messages.success(request, 'Emoción registrada con éxito.')
            return redirect('home')  # Redirige a la página de inicio
        else:
            messages.error(request, 'Hubo un error al registrar tu emoción. Por favor, intenta de nuevo.')
    else:
        form = EmotionEntryForm()

    yesterday = timezone.now().date() - timezone.timedelta(days=1)
    previous_entry = EmotionEntry.objects.filter(user=request.user, date__date=yesterday).first()

    previous_emotion = previous_entry.emotion_type if previous_entry else 'No hay datos del día anterior'

    context = {
        'form': form,
        'previous_emotion': previous_emotion,
        'date': timezone.now().date(),
        'time': timezone.localtime(timezone.now()).time()
    }
    return render(request, 'EmotionTracker/emotion_entry.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Recarga la instancia del usuario para actualizar el perfil.
            # Asegúrate de que el perfil está creado antes de acceder a él.
            Profile.objects.create(user=user)
            user.profile.user_type = form.cleaned_data.get('user_type')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'EmotionTracker/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'EmotionTracker/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def home_view(request):
    context = {
        'nav_options': ['Recursos', 'Libros', 'Videos', 'Coaching', 'Eventos'],
    }
    return render(request, 'EmotionTracker/home.html', context)


def emotion_entry_view(request):
    confirmation_message = None

    if request.method == 'POST':
        # Procesar el formulario de registro de emoción
        emotion_level = request.POST.get('emotion_level')
        user = request.POST.get('user')
        
        # Crear un nuevo registro de emoción en el modelo EmotionEntry
        emotion_entry = EmotionEntry(user=user, emotion_level=emotion_level)
        emotion_entry.save()
        
        # Agregar mensaje de confirmación
        confirmation_message = f"Emoción guardada: Usuario: {user}, Nivel de emoción: {emotion_level}"
        
    # Obtener las opciones para validar el progreso y volver al inicio
    options = {'validation_url': '/EmotionLog/ValidacionProgreso/', 'home_url': '/'}
    
    # Renderizar el formulario de registro de emoción utilizando el template específico
    return render(request, 'EmotionTracker/emotion_entry.html', {'confirmation_message': confirmation_message, 'options': options})



@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('home')  # Redirigir al usuario a la página de inicio después de enviar el feedback
    else:
        form = FeedbackForm()
    return render(request, 'EmotionTracker/feedback_thanks.html', {'form': form})

def progress_view(request):
    # Obtener los registros de emoción del usuario
    user = request.user  # Suponiendo que el usuario está autenticado
    emotion_entries = EmotionEntry.objects.filter(user=user)
    
    # Contar la cantidad de veces que se repite cada tipo de emoción
    emotion_counts = Counter(entry.emotion_type for entry in emotion_entries)
    
    # Generar la gráfica de barras
    fig, ax = plt.subplots()
    ax.bar(emotion_counts.keys(), emotion_counts.values())
    ax.set_xlabel('Tipo de Emoción')
    ax.set_ylabel('Cantidad')
    ax.set_title(f'Cantidad de veces que se repite cada emoción - {user.username}')
    
    # Convertir la gráfica a una imagen codificada en base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    context = {
        'emotion_chart': image_base64,
        'home_url': '/',  # Enlace para volver a la página de inicio
        'emotion_entry_url': '/EmotionLog/RegEmocion/',  # Enlace para registrar emociones
    }
    return render(request, 'EmotionTracker/progress.html', context)

def chatbot_view(request):
    return render(request, 'EmotionTracker/chatbot.html')


@login_required
def record_emotion_view(request):
    return render(request, 'EmotionTracker/record_emotion.html')

@csrf_exempt
def transcribe_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['file']
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                transcription = recognizer.recognize_google(audio_data, language='es-ES')
                
                # Analizar la emoción de la transcripción
                emotion = analyze_emotion(transcription)
                
                # Crear una nueva entrada de emoción y guardarla en la base de datos
                emotion_entry = EmotionEntry(
                    description=transcription,
                    emotion_type=emotion,
                    emotion_level=0  # Ajusta esto según tu modelo de datos
                )
                emotion_entry.save()
                
                return JsonResponse({'transcription': transcription})
            except sr.UnknownValueError:
                return JsonResponse({'transcription': 'No se pudo transcribir el audio.'}, status=400)
            except sr.RequestError:
                return JsonResponse({'transcription': 'Error en el servicio de transcripción.'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def get_emotion_analysis(description):
    url = 'https://fd1f-167-0-128-69.ngrok-free.app/analisis?text='
    response = requests.get(url + description)
    if response.status_code == 200:
        data = response.json()
        emotion = data.get('emotion')
        return emotion
    else:
        return None

def get_label(predict):
    labels = {
        0: "Triste",
        1: "Enojado",
        2: "Tranquilo",
        3: "Ansioso",
        4: "Feliz"
    }
    max_prob = np.max(predict)
    if max_prob < 0.6:
        return 'Triste'
    return labels[np.argmax(predict)]

def detect_emotion(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']

            cap = cv2.VideoCapture(video_file)

            with custom_object_scope({"KerasLayer": hub.KerasLayer}):
                modelo = load_model('modelo_entrenado.h5')

            emotions_detected = []

            while True:
                ret, frame = cap.read()

                if not ret:
                    break  
                img = cv2.resize(frame, (224, 224))
                img = np.expand_dims(img, axis=0)
                img = img / 255.0  

                prediccion = modelo.predict(img)
                label = get_label(prediccion[0])

                emotions_detected.append(label)

            cap.release()

            emotion_count = Counter(emotions_detected)
            most_common_emotion = emotion_count.most_common(1)[0][0]
            emotion_recording = EmotionRecording.objects.create(
                emotion_level=most_common_emotion,
                video_file=video_file,
                description="Descripción de la grabación",  
            )
            return redirect('home')  
    else:
        form = VideoUploadForm()

    return render(request, 'detect_emotion.html', {'form': form})