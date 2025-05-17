from sqlalchemy import Column, Integer, String
from .database import Base

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), index=True)
    question = Column(String(500))
    answer = Column(String(500))
    subject = Column(String(50))
