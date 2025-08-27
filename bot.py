import time
import requests
from dispatcher import TelegramDispatcher
from message_handler import MessageHandler


dispatcher = TelegramDispatcher()
offset = 0  #ID of the last message read

print("Bot is running. Press Ctrl+C to stop.")

while True:
    try:
        response = requests.get(
            f"{dispatcher.base_url}/getUpdates",
            params={"timeout": 30, "offset": offset + 1}, #waits 30 seconds. offset + 1 - only new messages
            timeout=35
        )

        if not response.ok: #check http on errors
            print(f"Telegram returned HTTP {response.status_code}")
            time.sleep(2)
            continue

        updates = response.json() #check if everything is correct (when an answer from the server came but smth can be wrong still)
        if not updates.get("ok"):
            print(f"Telegram logic error: {updates}")
            time.sleep(2)
            continue

        for update in updates["result"]:
            offset = update["update_id"]

            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "").strip()
            if not text: #if user sent a photo, video etc instead of text
                dispatcher.send_error(chat_id, "⚠️ Only text messages are supported.")
                continue

            response_text = MessageHandler.handle_message(text, chat_id)
            dispatcher.send_message(chat_id, response_text)

    except KeyboardInterrupt:
        print("Bot stopped by user.")
        break

    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(3)


