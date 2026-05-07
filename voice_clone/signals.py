# app_nomi/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Audio
from .services import convert_to_ai_voice
import threading



@receiver(post_save, sender=Audio)
def process_audio_on_upload(sender, instance, created, **kwargs):
    if created:
        # AI model ishlashi vaqt olganligi uchun asosiy saytni "qotirib" qo'ymaslik kerak.
        # Buning uchun alohida Thread yoki Celery ishlatgan ma'qul.
        # Hozircha oddiy Thread'da ishga tushiramiz:
        thread = threading.Thread(target=convert_to_ai_voice, args=(instance,))
        thread.start()