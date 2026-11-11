from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.misconception import Misconception, MisconceptionState
from app.models.misconception_history import MisconceptionHistoryEntry
from app.services.student_model.state_service import determine_next_state
from datetime import date

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "MentorCode API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

problems = [
    {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "Easy",
        "topic": "Arrays"
    },
    {
        "id": 2,
        "title": "Binary Search",
        "difficulty": "Easy",
        "topic": "Algorithms"
    },
    {
        "id": 3,
        "title": "Valid Parentheses",
        "difficulty": "Medium",
        "topic": "Stack"
    }
]

@app.get("/problems")
def get_problems():
    return problems

student_misconceptions = [
    Misconception(
        id=1,
        concept="Recursion",
        description="Missing or incorrect base case",
        state=MisconceptionState.PERSISTENT,
        evidence_count=3
    ),
    Misconception(
        id=2,
        concept="Arrays",
        description="Off-by-one errors",
        state=MisconceptionState.IMPROVING,
        evidence_count=4
    ),
    Misconception(
        id=3,
        concept="Binary Search",
        description="Incorrect boundary updates",
        state=MisconceptionState.RESOLVED,
        evidence_count=5
    )
]


@app.get("/students/{student_id}/misconceptions")
def get_student_misconceptions(student_id: int):
    return student_misconceptions

misconception_history = {
    1: [
        MisconceptionHistoryEntry(
            date="2026-11-01",
            state=MisconceptionState.POSSIBLE,
            evidence="Missing base case in a recursive sum problem"
        ),
        MisconceptionHistoryEntry(
            date="2026-11-04",
            state=MisconceptionState.PERSISTENT,
            evidence="Same issue appeared in a factorial problem"
        ),
        MisconceptionHistoryEntry(
            date="2026-11-08",
            state=MisconceptionState.IMPROVING,
            evidence="Base case was correct after receiving a hint"
        )
    ]
}

@app.get("/misconceptions/{misconception_id}/history")
def get_misconception_history(misconception_id: int):
    return misconception_history.get(misconception_id, [])

@app.post("/misconceptions/{misconception_id}/observe")
def observe_misconception(
    misconception_id: int,
    misconception_detected: bool
):
    misconception = next(
        (
            item for item in student_misconceptions
            if item.id == misconception_id
        ),
        None
    )

    if misconception is None:
        return {
            "error": "Misconception not found"
        }

    old_state = misconception.state

    new_state = determine_next_state(
        old_state,
        misconception_detected
    )

    misconception.state = new_state

    if misconception_detected:
        misconception.evidence_count += 1

    if misconception_id not in misconception_history:
        misconception_history[misconception_id] = []

    misconception_history[misconception_id].append(
        MisconceptionHistoryEntry(
            date=date.today(),
            state=new_state,
            evidence=(
                "Misconception detected in new submission"
                if misconception_detected
                else
                "Student solved the concept correctly"
            )
        )
    )

    return {
        "misconception_id": misconception_id,
        "old_state": old_state,
        "new_state": new_state,
        "misconception_detected": misconception_detected
    }