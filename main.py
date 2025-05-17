from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
import random

from .database import SessionLocal
from .models import Flashcard

from transformers import pipeline

# Load zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define possible subject labels
candidate_labels = [
    "Physics", "Biology", "Mathematics", "History", 
    "Geography", "Chemistry", "Computer Science", "English"
]

# Create FastAPI instance
app = FastAPI()


# Pydantic model for input
class FlashcardIn(BaseModel):
    student_id: str
    question: str
    answer: str


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to classify the subject using NLP
def classify_subject(text: str) -> str:
    result = classifier(text, candidate_labels)
    return result["labels"][0]


# POST /flashcard endpoint
@app.post("/flashcard")
def add_flashcard(flashcard: FlashcardIn, db: Session = Depends(get_db)):
    subject = classify_subject(flashcard.question)
    db_flashcard = Flashcard(
        student_id=flashcard.student_id,
        question=flashcard.question,
        answer=flashcard.answer,
        subject=subject
    )
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return {"message": "Flashcard added successfully", "subject": subject}


# GET /get-subject endpoint
@app.get("/get-subject")
def get_flashcards(student_id: str, limit: int = Query(default=5), db: Session = Depends(get_db)):
    all_cards = db.query(Flashcard).filter(Flashcard.student_id == student_id).all()
    
    # Group flashcards by subject
    subject_groups = {}
    for card in all_cards:
        subject_groups.setdefault(card.subject, []).append(card)
    
    selected = []
    subjects = list(subject_groups.keys())
    random.shuffle(subjects)

    # Select one flashcard per subject (until limit reached)
    for subject in subjects:
        if len(selected) >= limit:
            break
        card = random.choice(subject_groups[subject])
        selected.append({
            "question": card.question,
            "answer": card.answer,
            "subject": card.subject
        })

    return selected
