from django.contrib import admin
from .models import Audio




@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')