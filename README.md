# ⚔️ SpartanAudit

SpartanAudit is an automated, high-performance screening machine designed to assess the engineering quality and job relevancy of GitHub repositories. It replaces manual code review with a ruthless, AI-driven reconnaissance engine that distinguishes production-grade engineering from "Tutorial Hell."

---

## 🏗️ Architecture & Component Documentation

The system is split into two primary components. For specific implementation details, please refer to their respective documentation:

- **[Backend Documentation](./backend/README.md)**: Details the FastAPI intelligence engine, reconnaissance logic, and database schema.
- **[Frontend Documentation](./frontend/README.md)**: Details the React UI architecture, design system, and transparency protocols.

---

## 🔍 The Reconnaissance Engine

SpartanAudit does not clone repositories. Instead, it performs a targeted **High-Level Reconnaissance** via the GitHub API. It recursively scans directory structures (up to 2 levels deep, max 15 subdirectories) to identify "Proof of Engineering" artifacts.

### Artifact Detection Protocol
The engine specifically hunts for these file indicators:

#### 1. Source Code Proof (High Value)
*Verifies the presence of actual business logic and architecture.*
- **Entry Points**: `main.py`, `app.py`, `index.js`, `server.js`, `main.go`, `main.rs`
- **Database/Schema**: `database.py`, `models.py`, `schemas.py`, `prisma/schema.prisma`
- **Routing/Logic**: `routes.py`, `controllers.ts`, `services.py`, `utils.py`, `App.tsx`

#### 2. Infrastructure & DevOps
*Verifies deployability and environment management.*
- `Dockerfile`, `docker-compose.yml`, `Makefile`
- CI/CD: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`
- Hosting config: `vercel.json`, `netlify.toml`, `render.yaml`

#### 3. Machine Learning Artifacts
*Verifies actual data science work vs. empty claims.*
- **Notebooks**: `*.ipynb` (Analyzed as legitimate exploration tools)
- **Models**: `*.h5`, `*.pkl`, `*.pt`, `*.onnx` (Proof of training)
- **Data**: `*.csv`, `*.parquet`, `*.json`
- **MLOps**: `mlflow.yml`, `dvc.yaml`

#### 4. Dependency Manifests
*Verifies project complexity.*
- `package.json` (JS/TS), `requirements.txt` / `pyproject.toml` (Python)
- `go.mod`, `Cargo.toml`, `pom.xml`

---

## 🧠 The "Cynical Staff Engineer" Persona

The core intelligence is driven by a Large Language Model conditioned with a **"Cynical Staff Engineer"** persona. This persona is designed to be ruthless, efficient, and uncompromising, specifically trained to identify and reject "Tutorial Hell" projects (boilerplate code with no original engineering depth).

### The Persona's Mission
1. **Detect Production-Grade Engineering**: It looks for evidence of scalability, maintainability, and architectural thought, distinguishing real solutions from copy-pasted tutorials.
2. **Assign an Engineering Score (0-10)**: A brutal, objective rating based on the presence of tests, infrastructure config, and proper modularity.
3. **Calculate Relevancy Match**: If a Job Description is provided, it evaluates how well the repository demonstrates the specific skills required.
4. **Deliver a Brutal Critique**: A concise, no-nonsense paragraph highlighting exactly why the repo is good (or why it fails).
5. **Issue a Verdict**: It classifies every repo into one of three tiers:
    - **HIRE THIS SPARTAN**: Exemplary quality and strong JD match.
    - **GOOD DEV, WRONG FIT**: High engineering quality but low relevance to the role.
    - **TUTORIAL HELL**: Low quality, lack of depth, or obvious "cookie-cutter" project structure.

### Evaluation Logic
- **Source Code Proof**: Presence of `main.py`, `models.py`, or `routes.py` overrides "Tutorial" verdicts; it proves custom implementation.
- **ML Projects**: Jupyter notebooks and trained models are treated as first-class engineering artifacts, not penalized.
- **Web Projects**: Multi-folder structure (frontend/backend) + Dockerfiles substantially boost the Engineering Score.

---

## ⚠️ Audit Protocol Disclaimer

**SpartanAudit performs a metadata-based assessment.**

It evaluates:
- File existence and directory structure.
- Configuration complexity (docker-compose, CI pipelines).
- Technology stack breadth.
- README quality.

It does **NOT**:
- Perform static analysis (SAST).
- Execute the code.
- Read every line of every source file.

*Decisions are based on the presence of engineering signals that correlate with high-quality work, not the functional correctness of the code itself.*

---

## 🚀 Deployment

The entire stack is containerized for easy deployment.

### Prerequisites
- Docker & Docker Compose
- A valid API Key for the LLM provider (set as `GEMINI_API_KEY` in `backend/.env`)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/A-P-Shukla/SpartanAudit.git
cd SpartanAudit

# Start the stack
docker-compose up --build
```
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For inquiries regarding the SpartanAudit protocol or contributions, please open an issue in this repository.
