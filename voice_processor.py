import whisper
import os
from pydub import AudioSegment


class VoiceProcessor:
    def __init__(self, model_size="base"):
        # تحميل النموذج عند بدء التشغيل
        self.model = whisper.load_model(model_size)

    def convert_to_wav(self, audio_path):
        """تحويل ملف الصوت إلى صيغة WAV متوافقة تماماً مع Whisper"""
        try:
            # استخراج الامتداد
            file_extension = os.path.splitext(audio_path)[1].replace('.', '')

            # تحميل الملف الصوتي (يدعم ogg, opus, mp3, amr وغيرها)
            audio = AudioSegment.from_file(audio_path, format=file_extension)

            # تحويله إلى WAV وتردد 16000Hz (أفضل أداء للذكاء الاصطناعي)
            wav_path = audio_path.replace(file_extension, "wav")
            audio.export(wav_path, format="wav", parameters=["-ar", "16000", "-ac", "1"])

            return wav_path
        except Exception as e:
            print(f"❌ خطأ أثناء تحويل الصوت: {e}")
            return None

    def transcribe(self, audio_path):
        if not os.path.exists(audio_path):
            return "Error: File not found"

        # 1. تحويل الملف لصيغة قياسية أولاً لضمان الدقة
        print("🔄 جاري تهيئة الملف الصوتي...")
        standard_wav = self.convert_to_wav(audio_path)

        target_path = standard_wav if standard_wav else audio_path

        # 2. تنفيذ النسخ (Transcribe)
        print("🧠 جاري استخراج النص باستخدام Whisper...")
        result = self.model.transcribe(target_path, language='ar')

        # 3. تنظيف الملفات المؤقتة (اختياري للحفاظ على المساحة)
        if standard_wav and os.path.exists(standard_wav):
            os.remove(standard_wav)

        return result['text'].strip()

