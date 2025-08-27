from dataclasses import dataclass
from datetime import datetime

@dataclass
class MachineStatus:
    machine_id: str     # fe 2
    status: str         # active, free, unknown
    timestamp: datetime # date and time of the last change
