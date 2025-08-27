
from models.command import Command
from models.command_type import CommandType

class CommandParser:
    @staticmethod
    def parse_command(message_text: str) -> Command:
        """
        Parses the message text and returns a Command object.
        Recognized commands: /status <machine_id>, /help, /language, /free, /start
        """
        parts = message_text.strip().lower().split() #strrip - deletes all useless spaces and /n's, split - breaks the line into the list of words

        if not parts:
            raise ValueError("⚠️ Empty command.")

        command_type = parts[0].lstrip("/")

        if command_type == "status":
            if len(parts) == 1:
                # Command for asking the status of all of the machines: fe /status
                return Command(type=CommandType.status_all)
            elif len(parts) == 2:
                # Command for asking the status of the choosen machine: fe /status machine-001
                return Command(type=CommandType.status_one, machine_id=parts[1])
            else:
                raise ValueError("⚠️ Oops! I don't know this command! Please, check /help for more information")

        elif command_type in ["help","hilfe"]:
            return Command(type=CommandType.help)

        elif command_type in ["language","sprache"]:
            return Command(type=CommandType.lang)
        
        elif command_type == "start":
            return Command(type=CommandType.start)

        elif command_type in ["english", "german","englisch","deutsch"]:
            lang_code = "en" if command_type == "english" or command_type == "englisch" else "de"
            return Command(type=CommandType.set_lang, language=lang_code)

        else:
            raise ValueError(f"Unknown command: {command_type}\n❌ Error: Unbekannter Befehl: {command_type}")



