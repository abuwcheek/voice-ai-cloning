import librosa
import soundfile as sf
import numpy as np
import os
from django.conf import settings
from django.core.files.base import ContentFile



def process_voice_to_ai(audio_instance):
    """
    Ovozni sun'iy ko'rinishga keltirish va akustik tahlil qilish.
    """
    try:
        audio_instance.status = 'processing'
        audio_instance.save()

        # 1. Faylni yuklash
        path = audio_instance.original_file.path
        y, sr = librosa.load(path, sr=None)

        # 2. AI Transformatsiyasi (Pitch shifting)
        # Ovozni 4 yarim ton pastlatamiz (bu ko'pincha "sun'iylik" effektini beradi)
        # Haqiqiy RVC ishlatish uchun model.pth fayli kerak bo'ladi
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=-4)

        # 3. Spektral xususiyatlarni sug'urib olish (Dissertatsiya uchun eng muhim qism)
        # MFCC - Mel-frequency cepstral coefficients (Ovozning "barmoq izi")
        mfccs = librosa.feature.mfcc(y=y_shifted, sr=sr, n_mfcc=13)
        spectral_centroid = librosa.feature.spectral_centroid(y=y_shifted, sr=sr)
        
        # O'rtacha qiymatlarni hisoblash (JSONda saqlash uchun)
        features = {
            "mfcc_mean": float(np.mean(mfccs)),
            "spectral_centroid_mean": float(np.mean(spectral_centroid)),
            "sampling_rate": sr,
            "duration": float(librosa.get_duration(y=y, sr=sr)),
            "is_processed_by_ai": True
        }

        # 4. Natijani vaqtinchalik xotirada saqlash
        buffer = io.BytesIO()
        sf.write(buffer, y_shifted, sr, format='WAV')
        buffer.seek(0)

        # 5. Modelga saqlash
        file_name = f"ai_version_{audio_instance.id}.wav"
        audio_instance.generated_file.save(file_name, ContentFile(buffer.read()))
        
        audio_instance.spectral_features = features
        audio_instance.status = 'completed'
        audio_instance.save()

    except Exception as e:
        audio_instance.status = 'failed'
        audio_instance.save()
        print(f"Xatolik: {str(e)}")