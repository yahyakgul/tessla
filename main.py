import time
import requests
from bs4 import BeautifulSoup
import json
import pushbullet

# Pushbullet API anahtarın (ücretsiz hesap açıp alabilirsin)
PUSHBULLET_API_KEY = 'BURAYA_ANAHTARINI_YAZ'

def send_push_notification(title, body):
    pb = pushbullet.Pushbullet(PUSHBULLET_API_KEY)
    push = pb.push_note(title, body)

def check_inventory():
    url = "https://www.tesla.com/tr_TR/inventory/api/v1/inventory-results?query={%22query%22:{%22model%22:%22my%22,%22condition%22:%22new%22,%22options%22:{},%22location%22:%2234093%22},%22offset%22:0,%22count%22:50,%22sort%22:%22plh%22}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        vehicles = data.get('results', [])
        for vehicle in vehicles:
            if 'Standard' in vehicle.get('trim', ''):
                send_push_notification(
                    "Model Y Standart Range Bulundu!",
                    f"Link: https://www.tesla.com/tr_TR/inventory/new/my/{vehicle['VIN']}"
                )
                print("Standart Range bulundu! Bildirim gönderildi.")
            else:
                print("Şu anda Standart Range yok.")
    else:
        print("Tesla envanterine erişilemedi.")

def main():
    while True:
        check_inventory()
        time.sleep(60)  # 1 dakikada bir kontrol

if __name__ == "__main__":
    main()
