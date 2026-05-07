# serializers.py
from rest_framework import serializers
from .models import Audio



class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'



# views.py
from rest_framework import viewsets
from .models import Audio
from .serializers import AudioSerializer

class AudioViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer