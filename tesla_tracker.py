import subprocess
subprocess.run(["playwright", "install", "chromium"], check=True)
import time
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_IDS = [int(id_) for id_ in os.getenv("TELEGRAM_CHAT_IDS").split(",")]

MIN_PRICE = 1500000
MAX_PRICE = 2500000

def send_telegram_message(message):
    import requests
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        try:
            requests.post(url, data=data, timeout=10)
        except Exception as e:
            print(f"⚠️ Telegram mesajı gönderilemedi: {e}")

def check_inventory(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    url = "https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=34093&range=0"

    try:
        page.goto(url, timeout=60000)  # 60 sn bekleme süresi
        content = page.content()

        # Fiyatları al
        prices = []
        import re
        matches = re.findall(r"₺[\d\.\,]+", content)
        for match in matches:
            price_clean = int(match.replace("₺", "").replace(".", "").replace(",", ""))
            prices.append(price_clean)

        found = False
        for price in prices:
            if MIN_PRICE <= price <= MAX_PRICE:
                message = f"🚗 Tesla Model Y bulundu!\n💰 Fiyat: {price:,} TL\n🔗 Link: {url}"
                send_telegram_message(message)
                print(f"📩 Bildirim gönderildi! Fiyat: {price:,} TL")
                found = True

        if not found:
            print("🔍 Şu anda istenen fiyat aralığında araç bulunamadı.")

    except Exception as e:
        print(f"❗ Hata oluştu:\n{e}")
    finally:
        browser.close()

def main():
    with sync_playwright() as playwright:
        while True:
            check_inventory(playwright)
            time.sleep(60)

if __name__ == "__main__":
    main()
