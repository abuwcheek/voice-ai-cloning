from django.contrib import admin
from .models import Audio






@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    # Ro'yxatda nimalar ko'rinsin
    list_display = ('id', 'status', 'created_at', 'generated_file')
    
    # Faqat o'qish uchun maydonlar
    readonly_fields = ('created_at', 'updated_at', 'generated_file')