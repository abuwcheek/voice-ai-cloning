from django.apps import AppConfig

class VoiceCloneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voice_clone' # Ilovangiz nomi to'g'ri ekanini tekshiring

    def ready(self):
        import voice_clone.signals  # Signallarni ro'yxatga olish