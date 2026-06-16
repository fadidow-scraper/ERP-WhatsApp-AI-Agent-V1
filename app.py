from flask import Flask, request, jsonify
import requests
import os
import threading # أضفنا مكتبة خيوط المعالجة
import time
from main import run_system

app = Flask(__name__)

TEMP_DIR = "temp_voice_notes"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def background_worker(audio_url, sender):
    """وظيفة المعالجة في الخلفية لضمان سرعة رد الـ Webhook"""
    try:
        # إنشاء اسم فريد للملف باستخدام رقم المرسل والوقت لمنع التداخل
        file_name = f"voice_{sender}_{int(time.time())}.ogg"
        local_path = os.path.join(TEMP_DIR, file_name)

        # 1. تحميل الملف
        response = requests.get(audio_url, timeout=20)
        with open(local_path, 'wb') as f:
            f.write(response.content)

        print(f"✅ تم تحميل ملف {sender}، جاري المعالجة...")

        # 2. تشغيل المايسترو
        run_system(local_path, sender)

        # 3. حذف الملف بعد المعالجة للحفاظ على مساحة السيرفر
        if os.path.exists(local_path):
            os.remove(local_path)

    except Exception as e:
        print(f"❌ خطأ في المعالجة الخلفية لـ {sender}: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if data.get('event') == 'message_received':
        msg_data = data.get('data', {})

        if msg_data.get('type') == 'voice':
            audio_url = msg_data.get('url')
            sender = msg_data.get('from')

            print(f"📩 استلام طلب معالجة من: {sender}")

            # تشغيل المعالجة في خيط (Thread) منفصل والرد فوراً على UltraMsg
            process_thread = threading.Thread(target=background_worker, args=(audio_url, sender))
            process_thread.start()

    # الرد بـ 200 فوراً يخبر UltraMsg أننا استلمنا الرسالة بنجاح
    return jsonify({"status": "accepted", "message": "Processing in background"}), 200

if __name__ == "__main__":
    # threaded=True تزيد من قدرة Flask على تحمل الطلبات المتعددة
    app.run(port=5000, debug=False, threaded=True)

