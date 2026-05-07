from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AudioViewSet

# Router avtomatik ravishda /audio/ va /audio/1/ manzillarini yaratadi
router = DefaultRouter()
router.register(r'audio', AudioViewSet, basename='audio')



urlpatterns = [
    path('', include(router.urls)),
]