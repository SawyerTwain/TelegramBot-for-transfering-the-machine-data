from models.machine_status import MachineStatus
from typing import List

class ResponseFormatter:
    # language templates
    translations = {
        "en": {
            "start":"Welcome! My name is Laund 🧺😁\nWant to check if the washing machines are free, but too lazy to go down to the first floor?😴 Let me help you! Write /help and learn all the commands!🤙\n\nWillkommen! Mein Name ist Laund 🧺😁\nDu möchtest prüfen, ob die Waschmaschinen frei sind, bist aber zu faul, in den ersten Stock zu gehen?😴 Ich helfe dir! Schreibe /hilfe und lerne alle Befehle!🤙",
            "status_busy": "Washing machine {id} is currently busy. Please try again later.",
            "status_free": "Washing machine {id} is available. You can load your laundry!",
            "all_status": "📋 Status of all machines:",
            "help": "Available commands:\n• /status 2 – Status of washing machine no. 2\n• /status 3 – Status of washing machine no. 3\n• /status 4 – Status of washing machine no. 4\n• /status – check all machines\n• /language – change language\n• /help – this help message",
            "unknown": "Status of machine {id} is unknown.",
            "no_machines": "No machine data available.",
            "lang": "Choose a language:\n• English\n• German"
        },
        "de": {
            "start":"Willkommen! Mein Name ist Laund 🧺😁\nDu möchtest prüfen, ob die Waschmaschinen frei sind, bist aber zu faul, in den ersten Stock zu gehen?😴 Ich helfe dir! Schreibe /hilfe und lerne alle Befehle!🤙\n\nWelcome! My name is Laund 🧺😁\nWant to check if the washing machines are free, but too lazy to go down to the first floor?😴 Let me help you! Write /help and learn all the commands!🤙",
            "status_busy": "Waschmaschine {id} ist derzeit belegt. Bitte versuche es später erneut.",
            "status_free": "Waschmaschine {id} ist frei. Du kannst deine Wäsche laden!",
            "all_status": "📋 Status aller Maschinen:",
            "help": "Verfügbare Befehle:\n• /status 2 – Status der Waschmaschine Nr. 2\n• /status 3 – Status der Waschmaschine Nr. 3\n• /status 4 – Status der Waschmaschine Nr. 4\n• /status – Status aller Maschinen\n• /sprache – Sprache wechseln\n• /hilfe – Zeigt diese Hilfeübersicht an",
            "unknown": "Status der Maschine {id} ist unbekannt.",
            "no_machines": "Keine Maschinendaten verfügbar.",
            "lang": "Wähle eine Sprache:\n• Englisch\n• Deutsch"
        }
    }

    @classmethod
    def format_status_response(cls, machine: MachineStatus, lang: str = "en") -> str: #converts the status into a readable string

        

        lang_dict = cls.translations.get(lang, cls.translations["en"])  

        if machine.status == "active":
            return lang_dict["status_busy"].format(id=machine.machine_id)
        elif machine.status == "free":
            return lang_dict["status_free"].format(id=machine.machine_id)
        else:
            return lang_dict["unknown"].format(id=machine.machine_id)

    @classmethod
    def format_all_statuses(cls, machines: List[MachineStatus], lang: str = "en") -> str:
        lang_dict = cls.translations.get(lang, cls.translations["en"])

        if not machines:
            return lang_dict["no_machines"]

        lines = [lang_dict["all_status"]]
        for machine in machines:
            status_line = cls.format_status_response(machine, lang)
            lines.append(status_line)

        return "\n".join(lines)


    @classmethod
    def format_help(cls, lang: str = "en") -> str:

        return cls.translations.get(lang, cls.translations["en"])["help"]

    @classmethod
    def format_lang(cls, lang: str = "en") -> str:

        return cls.translations.get(lang, cls.translations["en"])["lang"]
    
    @classmethod
    def format_start(cls, lang: str = "en") -> str:

        return cls.translations.get(lang, cls.translations["en"])["start"]

 
