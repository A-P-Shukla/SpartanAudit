# SpartanAudit Backend

The SpartanAudit backend is a high-performance intelligence engine designed to assess the engineering quality and job-relevancy of GitHub repositories. It utilizes a custom "Cynical Staff Engineer" persona powered by Google Gemini to analyze repository metadata and project artifacts without requiring full repository cloning.

## Core Architecture

The backend is built with FastAPI and follows a modular design for scalability and maintainability.

### Primary Technologies
- **FastAPI**: Provides the asynchronous web framework.
- **Google Gemini (flash-lite-latest)**: Orchestrates the AI auditing logic.
- **LangChain**: Manages the integration between the LLM and the application logic.
- **SQLAlchemy**: Handles object-relational mapping for the PostgreSQL database.
- **Requests**: Manages high-level reconnaissance via the GitHub API.

## Project Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── crud.py          # Database CRUD operations
│   ├── database.py      # SQLAlchemy engine and session setup
│   ├── main.py          # API endpoints and reconnaissance logic
│   ├── models.py        # SQLAlchemy database models
│   └── schemas.py       # Pydantic models for request/response validation
├── Dockerfile           # Backend containerization configuration
├── requirements.txt     # Python dependencies
└── .env                 # Environment configuration (API keys, DB URLs)
```

## Reconnaissance Protocol

Instead of cloning entire repositories, the backend performs a targeted "High-Level Reconnaissance" to find "Proof of Engineering" artifacts.

### 1. Recursive Discovery
The engine recursively scans the repository structure up to 2 levels deep, discovering up to 15 subdirectories. This allows the system to identify complex monorepos (e.g., projects with separate /frontend and /backend folders).

### 2. Artifact Detection Categories
The system hunts for specific files to validate engineering claims:
- **Infrastructure**: Dockerfiles, docker-compose, CI/CD workflows (.github or .gitlab-ci), Makefiles.
- **Dependency Manifests**: package.json, requirements.txt (including variants like requirements_ml.txt), go.mod, Cargo.toml, pom.xml.
- **Source Code Proof**: Entry points (main.py, index.js), database schemas (database.py, prisma/schema), and architectural routing (routes.py, controllers.ts).
- **ML Artifacts**: Jupyter notebooks (.ipynb), trained models (.h5, .pt, .pkl), and datasets (CSV, Parquet, JSON).
- **Testing**: pytest.ini, jest.config.js, vitest.config.ts.

## API Endpoints

### POST /audit/
Triggers a fresh audit or returns a cached result.
- **Request Body**: `AuditRequest` (repo_url, job_description, force_reaudit).
- **Functionality**: Performs reconnaissance, sends data to Gemini, and persists the result.

### GET /history/
Retrieves the global history of all audits conducted.
- **Response**: List of `AuditResponse` objects containing scores, critiques, and verdicts.

### GET /audit/{audit_id}
Fetches a specific audit report by its unique ID.

## Database Schema

### Audits Table
- `id`: Integer (Primary Key)
- `repo_url`: String (Unique URL of the repository)
- `job_description`: Text (Optional input for relevancy matching)
- `engineering_score`: Float (0-10 score from the AI)
- `match_score`: Float (0-100% score, nullable)
- `critique`: Text (The AI's evaluation)
- `verdict`: String (The final classification)
- `found_files`: JSON (List of detected artifacts)
- `tech_stack`: JSON (Inferred technologies)
- `created_at`: DateTime (Timestamp)

## Environment Configuration

Create a .env file in the backend directory with the following variables:

```env
GEMINI_API_KEY="your_google_ai_key"
DATABASE_URL="postgresql://user:password@localhost:5432/spartan"
CORS_ORIGINS="http://localhost:3000"
```

## Setup and Installation

### Docker (Recommended)
Use the root level docker-compose.yml to spin up the entire stack:
```bash
docker-compose up --build
```

### Manual Local Setup
1. Create a virtual environment: `python -m venv env`
2. Activate the environment: `env\Scripts\activate` (Windows) or `source env/bin/activate` (Linux/macOS)
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn app.main:app --reload`
