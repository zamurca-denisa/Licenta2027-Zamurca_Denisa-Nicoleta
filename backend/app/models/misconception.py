from enum import Enum

from pydantic import BaseModel


class MisconceptionState(str, Enum):
    POSSIBLE = "possible"
    PERSISTENT = "persistent"
    IMPROVING = "improving"
    RESOLVED = "resolved"
    RECURRENCE = "recurrence"


class Misconception(BaseModel):
    id: int
    concept: str
    description: str
    state: MisconceptionState
    evidence_count: int