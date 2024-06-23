from django.db import models
from django.contrib.auth.models import User

class EmotionEntry(models.Model):
    user = models.CharField(max_length=100)
    emotion_level = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    emotion_type = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    activity = models.CharField(max_length=100, null=True, blank=True) 

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('cliente', 'Cliente'),
        ('psicologo', 'Psicólogo'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='cliente')

    def __str__(self):
        return self.user.username

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opinion = models.TextField()
    suggestions = models.TextField(default='')  # Definir un valor predeterminado aquí
    useful = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

class EmotionRecording(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    emotion_level = models.CharField(max_length=255)
    description = models.TextField()
    audio_file = models.FileField(upload_to='recordings/')
    video_file = models.FileField(upload_to='recordings/', null=True, blank=True)
    transcription = models.TextField(null=True, blank=True)
    analyzed_emotion = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Recording at {self.created_at}"