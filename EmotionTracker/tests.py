from django.test import TestCase

# Create your tests here.
# EmotionTracker/tests.py

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import EmotionEntry, Feedback

@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'nav_options' in response.context
    assert response.context['nav_options'] == ['Recursos', 'Libros', 'Videos', 'Coaching', 'Eventos']

@pytest.mark.django_db
def test_emotion_entry_view_get(client):
    response = client.get(reverse('emotion_entry'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_emotion_entry_view_post(client):
    data = {
        'emotion_level': '5',
        'user': 'testuser',
    }
    response = client.post(reverse('emotion_entry'), data)
    assert response.status_code == 200
    assert EmotionEntry.objects.filter(user='testuser', emotion_level='5').exists()
    assert 'Emoción guardada' in response.content.decode()

@pytest.mark.django_db
def test_progress_view(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    EmotionEntry.objects.create(user=user, emotion_level='5')

    response = client.get(reverse('progress'))
    assert response.status_code == 200
    assert 'emotion_chart' in response.context

@pytest.mark.django_db
def test_chatbot_view(client):
    response = client.get(reverse('chatbot'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_feedback_view_get(client):
    response = client.get(reverse('feedback'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_feedback_view_post(client):
    data = {
        'user': 'testuser',
        'feedback_text': 'This is a test feedback',
    }
    response = client.post(reverse('feedback'), data)
    assert response.status_code == 302  # Redirection to the thanks page
    assert Feedback.objects.filter(user='testuser', feedback_text='This is a test feedback').exists()

@pytest.mark.django_db
def test_feedback_thanks_view(client):
    response = client.get(reverse('feedback_thanks'))
    assert response.status_code == 200
    assert 'Gracias por tu Feedback' in response.content.decode()