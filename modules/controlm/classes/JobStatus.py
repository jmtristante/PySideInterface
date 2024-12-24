from enum import Enum

class JobStatus(Enum):
    OK = 0
    KO = 1
    WAITING = 2
    RUNNING = 3
    HOLDED = 4