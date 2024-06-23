from django.urls import path
from django.contrib import admin
from EmotionTracker.views import home_view, emotion_entry_view, progress_view, chatbot_view, signup, user_login, user_logout, emotion_entry, feedback_view, transcribe_audio, analyze_emotion,record_emotion_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    
    path('EmotionLog/RegEmocion/', emotion_entry_view, name='emotion_entry'),
    path('EmotionLog/ValidacionProgreso/', progress_view, name='progress'),
    path('EmotionLog/Chatbot/', chatbot_view, name='chatbot'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('emotion_entry/', emotion_entry, name='emotion_entry'),
    path('feedback/', feedback_view, name='feedback'),
    path('record_emotion/', record_emotion_view, name='record_emotion'),
    path('transcribe_audio/', transcribe_audio, name='transcribe_audio'),
    path('analyze_emotion/', analyze_emotion, name='analyze_emotion'),
] 
