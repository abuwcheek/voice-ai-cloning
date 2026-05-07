import os
import uuid
from django.db import models


def get_upload_path(instance, filename):
    """
    Fayl nomini unikal (takrorlanmas) qilish va audios/ papkasiga joylash.
    Masalan: audios/550e8400-e29b-41d4-a716-446655440000.wav
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('audios/', filename)



def get_generated_path(instance, filename):
    """Tayyorlangan (sun'iy) ovozlarni alohida generated/ papkasiga saqlash."""
    ext = filename.split('.')[-1]
    filename = f"gen_{uuid.uuid4()}.{ext}"
    return os.path.join('generated/', filename)



class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Audio(BaseModel):
    # Holatlar (Status) ro'yxati
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Ishlov berilmoqda'),
        ('completed', 'Muvaffaqiyatli yakunlandi'),
        ('failed', 'Xatolik yuz berdi'),
    ]

    # Asosiy maydonlar
    original_file = models.FileField(
        upload_to=get_upload_path, 
        verbose_name="Asl audio fayl"
    )
    generated_file = models.FileField(
        upload_to=get_generated_path, 
        blank=True, 
        null=True, 
        verbose_name="Sun'iy yaratilgan fayl"
    )
    
    # Qo'shimcha ma'lumotlar
    text = models.TextField(
        blank=True, 
        verbose_name="Nutq matni (STT)",
        help_text="Ovozdan ajratib olingan matn"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Jarayon holati"
    )
    
    error_message = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Xatolik xabari"
    )

    # MFCC va spektral tahlil natijalarini saqlash uchun JSON maydon
    # Bu maydon dissertatsiyangiz uchun eng muhim ma'lumotlarni o'zida saqlaydi
    mfcc_data = models.JSONField(
        blank=True, 
        null=True, 
        verbose_name="MFCC va Spektral ma'lumotlar"
    )

    class Meta:
        verbose_name = "Audio fayl"
        verbose_name_plural = "Audio fayllar"
        ordering = ['-created_at']

    def __str__(self):
        return f"ID: {self.id} | Status: {self.get_status_display()}"