from datetime import date

from pydantic import BaseModel

from app.models.misconception import MisconceptionState


class MisconceptionHistoryEntry(BaseModel):
    date: date
    state: MisconceptionState
    evidence: str