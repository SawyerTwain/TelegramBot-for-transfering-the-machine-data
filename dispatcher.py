import requests
import os #allows interaction with the operating system
from dotenv import load_dotenv  # to save telegram token securely

load_dotenv()  

class TelegramDispatcher:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.bot_token:
            raise EnvironmentError("🚫 TELEGRAM_BOT_TOKEN not set in .env")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    
    def send_message(self, chat_id: int, text: str) -> bool:
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if not response.ok:
                print(f"⚠️ Telegram API HTTP error: {response.status_code}")
                print(response.text)
                return False

            resp_data = response.json()
            if not resp_data.get("ok"):
                print(f"⚠️ Telegram API logic error: {resp_data}")
                return False

            return True

        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False

    def send_error(self, chat_id: int, error_text: str) -> bool:
        return self.send_message(chat_id, f"⚠️ {error_text}")

    def get_bot_info(self) -> dict:
        url = f"{self.base_url}/getMe"
        try:
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"❌ Failed to get bot info: {e}")
            return {}
