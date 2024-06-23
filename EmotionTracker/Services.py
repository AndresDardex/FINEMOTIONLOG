from .models import EmotionEntry, Feedback

def save_emotion_entry(user, emotion_level):
    # Lógica para guardar la entrada de emoción en la base de datos
    emotion_entry = EmotionEntry(user=user, emotion_level=emotion_level)
    emotion_entry.save()

def save_feedback_entry(user, feedback_text):
    # Lógica para guardar el feedback en la base de datos
    feedback_entry = Feedback(user=user, feedback_text=feedback_text)
    feedback_entry.save()