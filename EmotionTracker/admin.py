from django.contrib import admin
from .models import EmotionEntry
from .models import Feedback, EmotionRecording

class EmotionEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'emotion_type', 'date', 'description', 'location', 'activity')
    list_filter = ('emotion_type', 'date', 'user')
    search_fields = ('user', 'description', 'location', 'activity')

admin.site.register(EmotionEntry, EmotionEntryAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user','opinion', 'suggestions', 'useful', 'date')  # Mostrar estos campos en la lista de objetos
    list_filter = ('useful', 'date')  # Filtrar por estos campos
    search_fields = ('opinion', 'suggestions')  # Habilitar la búsqueda en estos campos

admin.site.register(Feedback, FeedbackAdmin)


class EmotionRecordingAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'emotion_level', 'description', 'audio_file', 'video_file', 'transcription', 'analyzed_emotion')
    list_filter = ('created_at', 'emotion_level')
    search_fields = ('description', 'transcription', 'analyzed_emotion')
admin.site.register(EmotionRecording, EmotionRecordingAdmin)