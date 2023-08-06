from enum import Enum

class RunStatus(Enum):
    SUCCESS = 0
    RUNNING = 1
    FAILED = 2
    PENDING = 3