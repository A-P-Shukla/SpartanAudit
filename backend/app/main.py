import os
import json
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from . import crud, models, schemas
from .database import engine, get_db

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IntelliQuiz API",
    description="API for generating quizzes from Wikipedia articles.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def scrape_wikipedia_content(url: str):
    try:
        headers = {'User-Agent': 'IntelliQuizApp/1.0 (test@example.com)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('h1', id='firstHeading')
        if not title:
            raise ValueError("Could not find article title (h1 with id='firstHeading').")
        
        content_div = soup.find('div', id='mw-content-text')
        if not content_div:
             raise ValueError("Could not find main article content div.")
        
        paragraphs = content_div.find_all('p', limit=20)
        text_content = "\n".join([p.get_text() for p in paragraphs if p.get_text().strip()])
        sections = [h2.get_text().replace('[edit]', '').strip() for h2 in content_div.find_all('h2')]
        
        return {
            "title": title.text, 
            "text_content": text_content, 
            "sections": sections,
            "raw_html": response.text
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {e} \nPlease enter a valid Wikipedia URL to begin.")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Error parsing page content: {e}")


def generate_quiz_with_llm(text_content: str, title: str):
    llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", google_api_key=os.getenv("GEMINI_API_KEY"), temperature=0.7)
    prompt_template = """
    Based on the following text about "{title}", generate a comprehensive JSON object for a quiz.
    The JSON object must strictly adhere to this structure: {{"summary": "...", "key_entities": {{"people": [], "organizations": [], "locations": []}}, "quiz": [{{"question": "...", "options": [], "answer": "...", "explanation": "...", "difficulty": "..."}}], "related_topics": []}}

    - "summary": A concise 2-3 sentence summary of the text.
    - "key_entities": A dictionary with "people", "organizations", and "locations" as keys. Each key should have a list of relevant string names.
    - "quiz": A list containing EXACTLY 10 quiz question objects. Each object MUST have these keys: "question", "options" (a list of exactly 4 unique strings), "answer" (one of the strings from the options list), "explanation" (a brief sentence on why the answer is correct), and "difficulty" (a string which must be one of 'easy', 'medium', or 'hard').
    - "related_topics": A list of 3-5 strings representing related Wikipedia topics.

    TEXT CONTENT:
    {text}
    
    IMPORTANT: You must respond with ONLY the raw JSON object. Do not include any surrounding text, comments, or markdown formatting like ```json. Your entire response must be a single, valid JSON object.
    """
    prompt = PromptTemplate.from_template(prompt_template)
    chain = prompt | llm | StrOutputParser()
    response_str = chain.invoke({"text": text_content, "title": title})
    
    try:
        clean_json_str = response_str.strip().lstrip("```json").rstrip("```")
        return json.loads(clean_json_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="The AI model returned a response that was not valid JSON. The response was: " + response_str)


# --- API Endpoints ---

@app.post("/generate-quiz/", response_model=schemas.Quiz, status_code=201)
def generate_quiz_from_url(req: schemas.QuizGenerationRequest, db: Session = Depends(get_db)):
    
    # Convert the special Pydantic HttpUrl to a plain string immediately.
    # Then, use this plain string variable everywhere else.
    url_as_string = str(req.url)

    db_quiz = crud.get_quiz_by_url(db, url=url_as_string)
    if db_quiz:
        return db_quiz

    scraped_data = scrape_wikipedia_content(url_as_string)
    if not scraped_data['text_content']:
        raise HTTPException(status_code=422, detail="Could not extract enough content from the article to generate a quiz.")

    llm_data = generate_quiz_with_llm(scraped_data["text_content"], scraped_data["title"])
    
    full_quiz_data = schemas.QuizCreate(
        url=url_as_string, # Use the plain string here
        title=scraped_data["title"],
        raw_html=scraped_data["raw_html"],
        summary=llm_data.get("summary", "No summary provided."),
        key_entities=llm_data.get("key_entities", {}),
        sections=scraped_data["sections"],
        quiz_data=llm_data.get("quiz", []),
        related_topics=llm_data.get("related_topics", []),
    )
    
    return crud.create_quiz(db=db, quiz_data=full_quiz_data)


@app.get("/quizzes/", response_model=List[schemas.Quiz])
def read_all_quizzes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieves a list of all previously generated quizzes from the database."""
    quizzes = crud.get_quizzes(db, skip=skip, limit=limit)
    return quizzes


@app.get("/validate-url/", response_model=dict)
def validate_url(url: str):
    """
    A lightweight endpoint for the frontend to quickly check if a URL is valid 
    and fetch its title for a better user experience.
    """
    try:
        headers = {'User-Agent': 'IntelliQuizApp/1.0 (test@example.com)'}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1', id='firstHeading')
        if title:
            return {"title": title.text}
        raise HTTPException(status_code=422, detail="URL is valid but no article title was found.")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=400, detail="Invalid or unreachable URL.")