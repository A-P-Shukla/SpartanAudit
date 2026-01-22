from sqlalchemy import Column, Integer, String, JSON, Text
from .database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text)
    
    # Store the generated quiz questions, options, etc.
    quiz_data = Column(JSON, nullable=False)
    
    # Store extracted entities and other metadata
    key_entities = Column(JSON)
    sections = Column(JSON)
    related_topics = Column(JSON)
    
    # Bonus: Store raw HTML for reference
    raw_html = Column(Text)