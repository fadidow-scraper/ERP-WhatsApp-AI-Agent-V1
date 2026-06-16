import requests
import json
from config import OPENROUTER_API_KEY
from database import Database  # استيراد ملف قاعدة البيانات


class AIAgent:
    def __init__(self):
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.db = Database()  # تهيئة قاعدة البيانات
        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "X-Title": "Fadi AI Agent"
        }

    def analyze_command(self, text, sender_number):
        # 1. جلب تاريخ المحادثة لتعزيز الفهم (سياق الكلام)
        history = self.db.get_history(sender_number)
        history_text = "\n".join([f"{h[0]}: {h[1]}" for h in history])

        # 2. تطوير الـ Prompt ليشمل التاريخ والتعليمات الصارمة
        prompt = f"""
        أنت مساعد ذكي لنظام ERP. مهمتك هي تحليل رسالة العميل الحالية بناءً على سياق المحادثة السابق وتحويلها إلى JSON.

        سياق المحادثة السابق:
        {history_text}

        الرسالة الجديدة: "{text}"

        المطلوب استخراجه بدقة:
        {{
            "action": "get_balance" أو "check_order" أو "unknown",
            "account_name": "اسم العميل المستهدف",
            "order_id": "رقم الطلب إن وجد"
        }}
        شروط الإجابة:
        - إذا كان الاسم غير موجود في الرسالة الجديدة ولكنه موجود في السياق السابق، استخدم الاسم من السياق.
        - أجب بصيغة JSON فقط.
        """

        data = {
            "model": "google/gemini-pro",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=data, timeout=15)
            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content']
            content = content.replace("```json", "").replace("```", "").strip()

            # 3. حفظ الرسالة الحالية في قاعدة البيانات للرجوع إليها مستقبلاً
            self.db.add_message(sender_number, text, "user")

            return content

        except Exception as e:
            print(f"Error in AI Logic: {e}")
            return json.dumps({"action": "unknown"})
