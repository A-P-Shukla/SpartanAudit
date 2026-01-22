# Backend Documentation: IntelliQuiz API

## Overview

The **IntelliQuiz API** is a robust FastAPI backend service designed to generate quizzes from Wikipedia articles using Large Language Models (LLMs - Gemini API). It provides advanced scraping, AI-powered quiz creation, persistent database storage, and RESTful endpoints for quiz management. This documentation describes its complete architecture, setup, and API details.


---

## Directory Structure
```
backend/
│
├── app/
│ ├── main.py # FastAPI app, endpoints, Wikipedia scraping, LLM logic
│ ├── models.py # SQLAlchemy database models
│ ├── schemas.py # Pydantic validation schemas
│ ├── database.py # DB config & session management
│ ├── crud.py # CRUD operations for quizzes
│ └── init.py # Package initialization
├── requirements.txt # Python dependency list
└── README.md
```

## Setup Instructions

**Prerequisites:**

- Python 3.9+
- Git
- A database supported by SQLAlchemy (e.g., SQLite for dev)
- Environment variable: `GEMINI_API_KEY` (Google Generative AI)

**Steps:**

1. **Clone the repository:**

    ```
    git clone https://github.com/A-P-Shukla/quiz-generator-project.git
    cd quiz-generator-project/backend
    ```

2. **Create and activate a virtual environment:**

    ```
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```
    pip install -r requirements.txt
    ```

4. **Create a `.env` file with your Gemini API key:**

    ```
    GEMINI_API_KEY=your_google_genai_api_key
    DATABASE_URL=sqlite:///./quiz.db            # Default: SQLite database
    ```

5. **Run migrations (if any):**
   - The backend will auto-create tables on startup for SQLite.

6. **Start the FastAPI server:**

    ```
    uvicorn app.main:app --reload
    ```

---

## Main Modules

### main.py

- **FastAPI instance:** App creation & configuration
- **CORS Middleware:** Allows cross-origin requests for frontend integration
- **Wikipedia Scraping:** Uses BeautifulSoup for structured content extraction
- **LLM Integration:** Gemini API (via LangChain) for generating quizzes
- **Endpoints:** `/generate-quiz/`, `/quizzes/`, `/validate-url/`

### models.py

- **Quiz Model:** SQLAlchemy ORM model for quizzes.
    - Attributes: URL, title, raw_html, summary, key_entities, sections, quiz_data, related_topics

### schemas.py

- **Quiz Schemas:** Data validation (Pydantic) for responses and requests.
- Ensures strict typing, structure, and security for all API inputs/outputs.

### database.py

- **Session management:** Handles DB engine creation and dependency injection for FastAPI routes.

### crud.py

- **CRUD Functions:** All database interactions for quiz creation, retrieval, and querying.

---

## API Endpoints

### 1. **Generate Quiz**

**POST** `/generate-quiz/`

- **Request Body:** JSON, validates Wikipedia URL.
- **Logic:**  
    - Scrapes Wikipedia article.
    - Sends content to Gemini LLM, receives structured quiz JSON.
    - Saves quiz, summary, key entities, and topics to the database.
    - Returns full quiz object.

**Response Model:**  
```
{
"url": "...",
"title": "...",
"raw_html": "...",
"summary": "...",
"key_entities": {
"people": [],
"organizations": [],
"locations": []
},
"sections": [],
"quiz_data": [
{
"question": "...",
"options": ["...", "...", "...", "..."],
"answer": "...",
"explanation": "...",
"difficulty": "easy|medium|hard"
}
],
"related_topics": []
}
```

### 2. **Get All Quizzes**

**GET** `/quizzes/`
- **Query Params:** `skip` (default 0), `limit` (default 100)
- **Returns:** List of all previously generated quizzes

### 3. **Validate Wikipedia URL**

**GET** `/validate-url/?url={url}`

- **Checks:** If the target URL is a valid Wikipedia article; extracts its title.
- **Returns:** `{ "title": "<Article Title>" }` or error.

---

## Core Logic Flow

1. **User submits Wikipedia URL**
2. `main.py` scrapes content and sections using BeautifulSoup
3. Sends cleaned content to Gemini LLM via LangChain for quiz generation
4. Receives JSON-formatted quiz (10 questions each with options, answer, explanation, difficulty, plus summary and key entities)
5. Saves quiz and metadata to database (SQLAlchemy Model)
6. Responds with comprehensive quiz object to API client

---

## Dependencies (requirements.txt)

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
- **Requests**: HTTP requests
- **Python-dotenv**: .env loading
- **BeautifulSoup4**: HTML parsing
- **LangChain & langchain_google_genai**: LLM orchestration
- *(additional conventional dependencies as per requirements)*

---

## Environment Variables

- `GEMINI_API_KEY`: Required for LLM queries
- `DATABASE_URL`: Optional; defaults to local SQLite

---

## Styling and Conventions

- Follows **PEP8** and modular code design.
- All endpoints strictly validate input and handle exceptions.
- Database models are normalized, extensible for other quiz sources.
- API response schemas ensure consistent structure & safe serialization.

---

## Development & Contribution Workflow

1. Fork and clone the repo
2. Create & activate a virtual environment
3. Install dependencies via `requirements.txt`
4. Use feature branches for new development
5. Ensure code linting and PEP8 compliance
6. Submit pull requests with clear commit messages and documentation updates

---

## Authors & Maintainers

- **Akhand Pratap Shukla**  
  [GitHub: A-P-Shukla](https://github.com/A-P-Shukla/)  
  [LinkedIn: Akhand Pratap Shukla](https://www.linkedin.com/in/akhand-pratap-shukla/)  
  Contact: akhandshukla36@gmail.com

---

## License

This project is open-source and available under the MIT License.

---
