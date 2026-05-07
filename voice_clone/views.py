# voice_clone/views.py

from rest_framework import viewsets
from .models import Audio  # Modelni bu yerda import qilamiz
from .serializers import AudioSerializer

# AGAR BU YERDA class Audio(models.Model): ... DEGAN QISM BO'LSA, UNI O'CHIRING!

class AudioViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer