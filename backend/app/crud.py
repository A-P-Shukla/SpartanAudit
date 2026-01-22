from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas

def get_quiz_by_url(db: Session, url: str):
    """Fetches a single quiz record from the DB by its URL."""
    return db.query(models.Quiz).filter(models.Quiz.url == url).first()

def get_quizzes(db: Session, skip: int = 0, limit: int = 100):
    """Fetches a list of all quizzes, ordered by the most recent."""
    return db.query(models.Quiz).order_by(desc(models.Quiz.id)).offset(skip).limit(limit).all()

def create_quiz(db: Session, quiz_data: schemas.QuizCreate) -> models.Quiz:
    """Creates a new quiz record in the database."""
    db_quiz = models.Quiz(**quiz_data.model_dump()) # Use model_dump for Pydantic v2
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz