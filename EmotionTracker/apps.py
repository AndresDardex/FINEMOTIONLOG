from django.apps import AppConfig


class EmotiontrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'EmotionTracker'

    def ready(self):
        import EmotionTracker.signals

class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        import your_app.signals
