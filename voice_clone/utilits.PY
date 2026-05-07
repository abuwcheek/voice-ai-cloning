import librosa
import numpy as np
import soundfile as sf
import os
from django.conf import settings



def process_voice_conversion(audio_instance):
    """
    Audio faylni sun'iy ko'rinishga o'tkazish logikasi.
    Bu yerda biz MFCC tahlili va Pitch shifting (ovoz tonini o'zgartirish) ishlatamiz.
    """
    try:
        # 1. Fayl yo'lini aniqlash
        input_path = audio_instance.original_file.path
        # Natijaviy fayl nomi: gen_uuid.wav
        output_filename = f"gen_{os.path.basename(input_path)}"
        output_path = os.path.join(settings.MEDIA_ROOT, 'generated', output_filename)
        
        # 'generated' papkasi mavjudligini tekshirish
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 2. Audioni yuklash (Librosa orqali)
        y, sr = librosa.load(input_path, sr=None)

        # --- ILMIY QISM (MFCC TAHLILI) ---
        # Biz bu yerda MFCC koeffitsiyentlarini olamiz (tahlil uchun)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        
        # --- O'ZGARTIRISH (VOICE CONVERSION DEMO) ---
        # Ovozni sun'iyroq qilish uchun uning tonini (pitch) 2 yarim ton pastlatamiz
        # Bu inson ovozini "robotik" yoki boshqa odam ovoziga yaqinlashtiradi
        y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=-2.5)

        # 3. Natijani saqlash
        sf.write(output_path, y_shifted, sr)

        # 4. Modelni yangilash
        audio_instance.generated_file = f"generated/{output_filename}"
        audio_instance.status = 'completed'
        audio_instance.text = "Ovoz muvaffaqiyatli tahlil qilindi va o'zgartirildi."
        audio_instance.save()

        return True

    except Exception as e:
        # Xatolik yuz bersa statusni yangilash
        audio_instance.status = 'failed'
        audio_instance.error_message = str(e)
        audio_instance.save()
        return False