from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any

# --- Request Models ---
# This model validates the incoming URL from the user. Using HttpUrl here is correct.
class QuizGenerationRequest(BaseModel):
    url: HttpUrl

# --- Response Models ---
# This defines the shape of the data sent back to the frontend.
class Quiz(BaseModel):
    id: int
    url: str # Use string for consistency in response
    title: str
    summary: str
    quiz_data: List[Dict[str, Any]]
    key_entities: Dict[str, List[str]]
    sections: List[str]
    related_topics: List[str]

    class Config:
        from_attributes = True

class QuizInfo(BaseModel):
    id: int
    url: str
    title: str

    class Config:
        from_attributes = True

# --- Internal Data Models ---
# This model is used to create the database entry. The `url` field MUST be a plain string
# because this is what SQLAlchemy will pass to the database driver.
class QuizCreate(BaseModel):
    url: str 
    title: str
    summary: str
    quiz_data: List[Dict[str, Any]]
    key_entities: Dict[str, List[str]]
    sections: List[str]
    related_topics: List[str]
    raw_html: str