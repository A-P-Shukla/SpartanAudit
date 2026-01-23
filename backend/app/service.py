import os
import json
from typing import Optional
from fastapi import HTTPException
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_audit_report(metadata: dict, jd: Optional[str]):
    llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest", google_api_key=os.getenv("GEMINI_API_KEY"), temperature=0.7)
    
    prompt_template = """
    You are a Cynical Staff Engineer at a high-growth startup. Your job is to audit a candidate's GitHub repository.
    Be ruthless, efficient, and uncompromising. You see through "Tutorial Hell" projects.

    MISSION:
    1. Determine if this is "Production-Grade Engineering" or "Spaghetti Code/Tutorial".
    2. Provide a 0-10 Engineering Score.
    3. (Optional) If a Job Description (JD) is provided, calculate a 0-100% Relevancy Match. If NO JD is provided, match_score MUST be null.
    4. Provide a brutal one-paragraph critique.
    5. Assign a Verdict:
       - "HIRE THIS SPARTAN": High Quality + (High Match OR No JD provided).
       - "GOOD DEV, WRONG FIT": High Quality + Low Match (Only if JD is provided).
       - "TUTORIAL HELL": Low Quality (regardless of JD).

    DATA FOUND:
    - Files detected: {found_files}
    - Tech stack identified: {tech_stack}
    - ML/Data Science Artifacts: {ml_artifacts}
    - **SOURCE CODE PROOF**: {source_code_files}
    - README Content: {readme_content}

    CRITICAL EVALUATION RULES:
    
    **SOURCE CODE PROOF (Use This First):**
    - If main.py, app.py, database.py, models.py, routes.py, or App.tsx are found: THIS IS REAL CODE, NOT A TUTORIAL.
    - Source files in multiple directories = modular architecture = GOOD.
    - database.py or schema.prisma = they're using a real database, not SQLite hello-world.
    - migrations/ folder = production-ready data management.
    - DO NOT critique "lack of code evidence" if source_code_files is populated.
    
    **For ML/Data Science Projects:**
    - Jupyter notebooks (.ipynb) are LEGITIMATE tools for exploration and analysis, NOT tutorial markers.
    - Presence of trained models (.h5, .pkl, .pt, .onnx) indicates ACTUAL work, not copy-paste.
    - Dataset files (train.csv, test.csv, *.parquet) show real data handling.
    - ML project structure is different from web apps; don't penalize for lack of Dockerfile if there are notebooks and models.
    - Score HIGHER if: custom models, data pipelines, experimentation notebooks, MLOps configs (mlflow, dvc).
    - Score LOWER if: only a single "hello world" notebook with no datasets or models.
    
    **For Web/Backend Projects:**
    - Dockerfiles, CI/CD workflows, and multi-tier architecture are strong indicators.
    - Multiple dependency files (frontend + backend) show real full-stack work.
    - Score HIGHER if: production configs, environment management, deployment manifests.
    - Score LOWER if: single README, no infra, or just boilerplate create-react-app.
    
    **General Red Flags (Tutorial Hell):**
    - README is 90% setup instructions with no actual code evidence.
    - Only package.json/requirements.txt with no actual source files detected.
    - Claims of "ML pipeline" but no notebooks, models, or datasets found.
    
    **General Green Flags (Production-Grade):**
    - Multiple proof points: tests + infra + dependencies.
    - Evidence of iteration: multiple model versions, data preprocessing scripts.
    - Real deployment artifacts: Docker, CI/CD, or cloud configs.

    {jd_section}

    RESPONSE FORMAT: Respond with ONLY raw JSON. No markdown prefix.
    {{
        "engineering_score": float,
        "match_score": float (null if no JD),
        "critique": "string (brutal paragraph)",
        "verdict": "string",
        "tech_stack_inferred": ["string"]
    }}
    """
    
    jd_section = f"**JOB DESCRIPTION:**\n{jd}" if jd else "NO JOB DESCRIPTION PROVIDED."

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["found_files", "tech_stack", "ml_artifacts", "source_code_files", "readme_content", "jd_section"]
    )
    
    chain = prompt | llm | StrOutputParser()
    
    try:
        response_str = chain.invoke({
            "found_files": metadata["found_files"],
            "tech_stack": metadata["tech_stack"],
            "ml_artifacts": metadata.get("ml_artifacts", []),
            "source_code_files": metadata.get("source_code_files", []),
            "readme_content": metadata["readme_content"],
            "jd_section": jd_section
        })
        
        clean_json_str = response_str.strip().lstrip("```json").rstrip("```")
        return json.loads(clean_json_str)
    except Exception as e:
        # Fallback error handling if LLM fails or returns bad JSON
        raise HTTPException(status_code=500, detail=f"The AI brain glitched. Error: {str(e)}")
