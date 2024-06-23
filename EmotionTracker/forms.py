from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmotionEntry
from .models import Feedback
from .models import EmotionRecording

class SignUpForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('cliente', 'Cliente'),
        ('psicologo', 'Psicólogo'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, label='Tipo de usuario')

    class Meta:
        model = User
        fields = ('username', 'user_type', 'password1', 'password2', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user

class EmotionEntryForm(forms.ModelForm):
    class Meta:
        model = EmotionEntry
        fields = ['emotion_level', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe tus emociones aquí...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emotion_level'].initial = 3
        self.fields['emotion_level'].widget.attrs.update({'class': 'form-control'})
        

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['opinion', 'suggestions', 'useful']  # Añadir los campos necesarios
        widgets = {
            'opinion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'suggestions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'useful': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
        }


class EmotionRecordingForm(forms.ModelForm):
    class Meta:
        model = EmotionRecording
        fields = ['emotion_level', 'description', 'audio_file', 'video_file']

from django import forms

class VideoUploadForm(forms.Form):
    video_file = forms.FileField(label='Seleccionar archivo de video')

