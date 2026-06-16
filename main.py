from voice_processor import VoiceProcessor
from ai_logic import AIAgent
from erp_connector import ERPConnector
from whatsapp_api import WhatsAppAPI
from database import Database  # أضفنا قاعدة البيانات هنا أيضاً
import json


def run_system(audio_file, sender_number):
    # 1. تهيئة الوحدات
    vp = VoiceProcessor()
    ai = AIAgent()
    erp = ERPConnector()
    wa = WhatsAppAPI()
    db = Database()  # تهيئة الذاكرة

    print(f"--- بدأت معالجة الرسالة من: {sender_number} ---")

    # 2. تحويل الصوت لنص
    text = vp.transcribe(audio_file)
    if "Error" in text:
        print(f"❌ خطأ: {text}")
        return

    print(f"🎤 النص المستخرج: {text}")

    # 3. فهم الأمر عبر الذكاء الاصطناعي (تم تمرير رقم المرسل للذاكرة)
    ai_raw_response = ai.analyze_command(text, sender_number)

    try:
        ai_data = json.loads(ai_raw_response)
    except:
        ai_data = {"action": "unknown"}

    print(f"🤖 تحليل الأمر: {ai_data}")

    # 4. تنفيذ الأمر والربط مع ERP
    if ai_data.get('action') == "get_balance":
        name = ai_data.get('account_name', 'غير معروف')
        balance_info = erp.get_balance(name)
        response_msg = f"مرحباً {name}، رصيدك الحالي هو {balance_info['balance']} {balance_info['currency']}."
    else:
        response_msg = "عذراً، لم أفهم طلبك بوضوح، هل يمكنك إعادة صياغة الطلب أو تحديد الاسم؟"

    # 5. حفظ رد البوت في الذاكرة (ليتذكره في المرة القادمة)
    db.add_message(sender_number, response_msg, "assistant")

    # 6. إرسال الرد عبر واتساب
    print(f"📤 إرسال الرد: {response_msg}")
    wa.send_message(sender_number, response_msg)
    print("--- تمت العملية بنجاح ---")


if __name__ == "__main__":
    # تجربة يدوية
    run_system("temp_voice_notes/test.ogg", "963936334225")
