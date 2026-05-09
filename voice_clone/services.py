import librosa
import numpy as np
import soundfile as sf
import os
from django.conf import settings



def process_voice_to_ai(instance):
    try:
        # 1. Holatni yangilash
        instance.status = 'processing'
        instance.save()

        # 2. Yo'llarni sozlash
        input_path = instance.original_file.path
        gen_filename = f"cloned_{os.path.basename(input_path)}"
        gen_relative_path = os.path.join('generated', gen_filename)
        output_path = os.path.join(settings.MEDIA_ROOT, gen_relative_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 3. Ovozni yuklash (Asl sifatda)
        y, sr = librosa.load(input_path, sr=None)

        # --- ILMIY ISH UCHUN MUHIM QISMLAR ---
        
        # A. Shovqinni filtrlash (Pre-emphasis)
        # Bu yuqori chastotalarni kuchaytirib, nutqni aniqroq qiladi
        y_filt = librosa.effects.preemphasis(y)

        # B. Formantlarni saqlagan holda pitch o'zgartirish
        # n_stepsni juda kichik (masalan -0.3) ushlaymiz, 
        # shunda "robot" ovozi chiqib qolmaydi
        y_shifted = librosa.effects.pitch_shift(y_filt, sr=sr, n_steps=-0.3)

        # C. Spektral qobiqni silliqlash (Time-stretching orqali biroz "jon" kiritish)
        # Ovoz tezligini 1% ga sekinlashtirish inson qulog'iga tabiiyroq tuyuladi
        y_stretched = librosa.effects.time_stretch(y_shifted, rate=0.99)

        # D. Normallashtirish
        # Peak-normalization: ovoz xirillab qolmasligi uchun
        y_final = librosa.util.normalize(y_stretched)

        # 4. Faylni saqlash
        sf.write(output_path, y_final, sr)

        # 5. Natijani bazaga yozish
        instance.generated_file = gen_relative_path
        instance.status = 'completed'
        instance.save()

    except Exception as e:
        instance.status = 'failed'
        instance.error_message = str(e)
        instance.save()