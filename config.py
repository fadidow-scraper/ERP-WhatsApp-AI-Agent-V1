import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

# --- إعدادات الذكاء الاصطناعي (AI & Voice) ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# --- إعدادات واتساب (UltraMsg API) ---
ULTRAMSG_INSTANCE_ID = os.getenv("ULTRAMSG_INSTANCE_ID")
ULTRAMSG_TOKEN = os.getenv("ULTRAMSG_TOKEN")

# --- إعدادات نظام الـ ERP ---
# ملاحظة: سنستخدم هذا الرابط كمحاكاة (Mock) في البداية
ERP_BASE_URL = "https://client-erp-system.com"
ERP_API_KEY = os.getenv("ERP_API_KEY")

# --- إعدادات تقنية واستقرار النظام ---
MAX_RETRIES = 3
RETRY_DELAY = 5
TIMEOUT = 30

# --- إعدادات الملفات والمجلدات ---
DB_FILE = "whatsapp_agent.db"
TEMP_VOICE_DIR = "temp_voice_notes/"

# التأكد من وجود مجلد الملفات الصوتية عند التشغيل
if not os.path.exists(TEMP_VOICE_DIR):
    os.makedirs(TEMP_VOICE_DIR)

# --- ترويسات الطلبات (Headers) ---
HEADERS = {
    'Authorization': f'Bearer {ERP_API_KEY}',
    'Content-Type': 'application/json',
    'User-Agent': 'Fadi-AI-Agent-V1'
}
