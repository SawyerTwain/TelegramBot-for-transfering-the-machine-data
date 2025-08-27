
from command_parser import CommandParser
from api_client import Apiclient
from response_formatter import ResponseFormatter
from language_manager import LanguageManager 
from models.command_type import CommandType 
import requests

api = Apiclient()

class MessageHandler:
    @staticmethod
    def handle_message(text: str, user_id: int) -> str:  #receives reply from the user and returns a line
        try:
            command = CommandParser.parse_command(text)  #parse into Command(status, machine_id)
            lang = LanguageManager.get_lang(user_id)  

            if command.type == CommandType.status_one:
                status = api.get_machine_status(command.machine_id)
                if not status:
                    return "⚠️ Could not retrieve machine status. Please try again later."
                return ResponseFormatter.format_status_response(status, lang)

            elif command.type == CommandType.status_all:
                machines = api.get_all_statuses()
                if not machines:
                    return "⚠️ Could not retrieve statuses. Please try again later."
                return ResponseFormatter.format_all_statuses(machines, lang)

            elif command.type == CommandType.help:
                return ResponseFormatter.format_help(lang)
            
            elif command.type == CommandType.start:
                return ResponseFormatter.format_start(lang)

            elif command.type == CommandType.lang:
                return ResponseFormatter.format_lang(lang)

            elif command.type == CommandType.set_lang:
                LanguageManager.set_lang(user_id, command.language)
                return (
                    "✅ Language set to English." if command.language == "en"
                    else "✅ Sprache wurde auf Deutsch eingestellt."
                )

            else:
                return "🤷 Unknown command."

        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                return "⚠️ Authorization error: invalid credentials."
            elif http_err.response.status_code == 404:
                return "⚠️ Device not found."
            else:
                return "⚠️ Server returned an error. Please try again later."

        except requests.exceptions.Timeout:
            return "⚠️ Server timeout. Please try again later."

        except Exception:
            return "⚠️ Unexpected error occurred. Please try again later."
        
        