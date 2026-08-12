import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# ==========================================
# 1. بياناتك الشخصية (يجب تعبئتها بدقة)
# ==========================================
TELEGRAM_TOKEN = "8906163542:AAFcuBGBuKU5yqgTBZ9vsWQR5PfdDa2KtSY"
TELEGRAM_CHAT_ID = "7214076587"
def send_telegram_message(text):
    """إرسال إشعار على تليجرام"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={text}"
    try:
        requests.get(url)
    except Exception as e:
        print("❌ فشل إرسال الإشعار:", e)

def main():
    print("🚀 البوت يعمل الآن من سيرفر GitHub...")
    
    # إعداد المتصفح المخفي
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # قراءة آخر مشروع تم إرساله من ملف النص (عشان ميكررش الرسايل)
    last_url = ""
    if os.path.exists("last_project.txt"):
        with open("last_project.txt", "r", encoding="utf-8") as f:
            last_url = f.read().strip()

    try:
        driver.get("https://nafezly.com/projects")
        driver.implicitly_wait(10) # انتظار تحميل الصفحة
        
        # اصطياد أحدث مشروع
        project_element = driver.find_element(By.XPATH, "//div[contains(@class, 'text-truncate')]/a")
        current_project_title = project_element.text
        project_url = project_element.get_attribute("href")
        
        # لو المشروع جديد
        if project_url != last_url:
            print(f"🔔 تم العثور على مشروع جديد: {current_project_title}")
            
            # إرسال الرسالة
            msg = f"🔔 مشروع جديد على نفذلي!\n\n📌 العنوان: {current_project_title}\n🔗 الرابط: {project_url}"
            send_telegram_message(msg)
            
            # حفظ الرابط الجديد في الملف
            with open("last_project.txt", "w", encoding="utf-8") as f:
                f.write(project_url)
            print("✅ تم الإرسال والحفظ بنجاح.")
        else:
            print("🔄 لا توجد مشاريع جديدة.")
            
    except Exception as e:
        print("❌ حدث خطأ:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()