from dataclasses import dataclass
from typing import Optional
from models.command_type import CommandType

@dataclass
class Command:
    type: CommandType
    machine_id: Optional[str] = None
    language: Optional[str] = None  # only for lang
