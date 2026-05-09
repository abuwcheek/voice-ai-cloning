from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Audio
from .services import process_voice_to_ai
import threading




@receiver(post_save, sender=Audio)
def trigger_ai_processing(sender, instance, created, **kwargs):
    if created:
        # Bu qator AI funksiyasini orqa fonda ishga tushiradi
        thread = threading.Thread(target=process_voice_to_ai, args=(instance,))
        thread.start()