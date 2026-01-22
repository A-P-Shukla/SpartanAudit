# ⚔️ SpartanAudit

**Automated Code Quality & Relevancy Screener**

> "To save the TechKareer team hundreds of hours by automatically identifying whether a candidate's GitHub project is 'Production-Grade Engineering' or 'Spaghetti Code.'"

---

## 🚀 The Mission
SpartanAudit is built for recruiters and hiring managers who don't have time to clone every repository. It acts as a **Cynical Staff Engineer**, providing a ruthless, automated, and uncompromising audit of any GitHub project in seconds.

## 🧠 The Engine: Three-Step Intelligence Pipeline

### Step A: The Reconnaissance (Lazy Fetching)
We don't download the whole repo. We target the "Proof of Engineering":
- **Documentation Check**: No `README.md`? Automatic failure.
- **Infrastructure Check**: Detects `Dockerfile`, `docker-compose.yml`, or `.github` workflows.
- **Stack Check**: Identifies `package.json`, `requirements.txt`, `go.mod`, etc., to map complexity.

### Step B: The Assessment (AI Auditor)
Powered by **Google Gemini**, the system evaluates:
- **Engineering Quality**: Is it a real solution or just another "To-Do List" tutorial?
- **Relevancy Check**: (Optional) Matches the repo against your provided Job Description.

### Step C: The Report Card
Get a definitive hierarchy of results:
- 🟩 **HIRE THIS SPARTAN**: High Quality + High Match.
- 🟨 **GOOD DEV, WRONG FIT**: High Quality + Low Match.
- 🟥 **TUTORIAL HELL**: Low Quality.

## 🛠️ Tech Stack
- **Frontend**: React (Modern, Ruthless UI)
- **Backend**: FastAPI (Python)
- **AI**: Google Gemini (via LangChain)
- **Database**: PostgreSQL (SQLAlchemy)

## ⚖️ Why SpartanAudit?
- **Fast**: Lazy fetching means results in seconds.
- **Language Agnostic**: Works for Rust, Python, JS, Go, and more.
- **Decision-Focused**: Built to help you make a "Snap Decision" in 5 seconds.

---
*Built for the bold.*
