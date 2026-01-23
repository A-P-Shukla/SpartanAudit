import os
import requests
from urllib.parse import urlparse
from fastapi import HTTPException

# Expanded file patterns with common variants
FILES_TO_CHECK = {
    "readme": ["README.md", "readme.md", "README.markdown", "README.rst", "README.txt"],
    "infra": [
        "Dockerfile", "dockerfile", 
        "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml",
        ".github/workflows/main.yml", ".github/workflows/ci.yml", ".github/workflows/build.yml",
        ".github/workflows/test.yml", ".github/workflows/deploy.yml",
        "Makefile", "makefile",
        ".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml",
        "vercel.json", "netlify.toml", "render.yaml"
    ],
    "stack": [
        # Python variants
        "requirements.txt", "requirements-dev.txt", "requirements_dev.txt",
        "requirements-ml.txt", "requirements_ml.txt", "requirements-backend.txt", "requirements_backend.txt",
        "requirements-prod.txt", "requirements_prod.txt", "pyproject.toml", "setup.py", "Pipfile",
        # JS/TS
        "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        # Other languages
        "go.mod", "go.sum", "Cargo.toml", "Cargo.lock",
        "pom.xml", "build.gradle", "build.gradle.kts",
        "Gemfile", "Gemfile.lock", "composer.json", "composer.lock"
    ],
    "tests": [
        "pytest.ini", "setup.cfg", "tox.ini", "jest.config.js", "jest.config.ts",
        "vitest.config.ts", ".eslintrc", ".eslintrc.js", ".prettierrc"
    ],
    "ml_artifacts": [
        # Jupyter Notebooks
        "*.ipynb", "notebook.ipynb", "analysis.ipynb", "exploration.ipynb",
        # Model files
        "*.h5", "*.pkl", "*.pickle", "*.pt", "*.pth", "*.onnx", "*.pb", "*.joblib",
        "model.h5", "best_model.pt", "final_model.pkl",
        # Dataset indicators (common filenames)
        "train.csv", "test.csv", "data.csv", "dataset.csv", "*.parquet",
        "train.json", "test.json", "data.json",
        # ML config files
        "config.yaml", "config.yml", "mlflow.yml", "dvc.yaml", "params.yaml"
    ],
    "source_code": [
        # Entry points - Proof the app actually runs
        "main.py", "app.py", "server.py", "manage.py",
        "index.js", "server.js", "index.ts", "main.ts",
        "main.go", "main.rs",
        # Database schemas - Kills "SQLite tutorial" myth
        "database.py", "db.py", "connection.py",
        "prisma/schema.prisma", "drizzle.config.ts",
        "alembic/versions/*.py", "migrations/*.py",
        # Models & schemas - Complexity proof
        "models.py", "models.ts", "schema.py", "schemas.py",
        "entities.py", "entity.py",
        # Routing/Architecture - Not just one file
        "routes.py", "router.py", "urls.py", "views.py",
        "router.js", "routes.ts", "controllers.ts",
        "App.tsx", "App.jsx", "app/layout.tsx",
        # Business logic
        "services.py", "service.py", "utils.py", "helpers.py"
    ]
}

def get_github_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/vnd.github.v3+json"
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def get_github_raw_url(repo_url: str, file_path: str, branch: str = "main"):
    """Converts a GitHub repo URL into a raw content URL."""
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        return None
    owner, repo = path_parts[0], path_parts[1]
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"

def get_all_directories_recursive(repo_url: str, path: str = "", depth: int = 0, max_depth: int = 2, max_total_dirs: int = 15):
    """
    Recursively fetches ALL directories in a repository up to max_depth.
    Returns a list of directory paths (e.g., ['', 'backend/', 'backend/app/', 'frontend/src/']).
    LIMITED to prevent timeouts on large repos.
    """
    if depth > max_depth:
        return []
    
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        return []
    owner, repo = path_parts[0], path_parts[1]
    
    dirs = [path] if path else [""]  # Include current path
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    try:
        res = requests.get(api_url, headers=get_github_headers(), timeout=2)  # Strict 2-second timeout
        if res.status_code == 200:
            contents = res.json()
            for item in contents:
                if item.get("type") == "dir":
                    # Stop if we've already found too many directories
                    if len(dirs) >= max_total_dirs:
                        return dirs
                    
                    subdir_path = f"{item['path']}/"
                    dirs.append(subdir_path)
                    # Recursively get nested directories
                    nested = get_all_directories_recursive(repo_url, item['path'], depth + 1, max_depth, max_total_dirs)
                    dirs.extend(nested)
                    
                    # Check again after recursion
                    if len(dirs) >= max_total_dirs:
                        return dirs
    except:
        pass
    
    return list(set(dirs))  # Remove duplicates

def fetch_repo_metadata(repo_url: str):
    """
    Checks for key 'Proof of Engineering' files without cloning.
    Recursively scans ALL subdirectories up to 2 levels deep.
    Supports variant filenames (e.g., requirements_ml.txt, requirements_backend.txt).
    """
    
    # Recursively fetch ALL subdirectories (up to 3 levels deep)
    all_dirs = get_all_directories_recursive(repo_url)
    
    found_files = []
    readme_content = ""
    tech_stack = []
    ml_artifacts = []  # Track ML/DS specific files
    source_code_files = []  # Track actual source code
    
    # Try 'main' then 'master' branches
    for branch in ["main", "master"]:
        current_found = []
        for dir_path in all_dirs:
            for category, filenames in FILES_TO_CHECK.items():
                for filename in filenames:
                    # Skip .github paths if we're not at root (they're always at root)
                    if filename.startswith(".github") and dir_path:
                        continue
                    
                    full_path = f"{dir_path}{filename}"
                    raw_url = get_github_raw_url(repo_url, full_path, branch)
                    if not raw_url: continue
                    
                    try:
                        res = requests.get(raw_url, headers=get_github_headers(), timeout=2)
                        if res.status_code == 200:
                            current_found.append(full_path)
                            # Prefer root README, but take subdir if not found
                            if category == "readme" and not readme_content:
                                readme_content = res.text[:5000]
                            if category == "stack":
                                tech_stack.append(full_path)
                            if category == "ml_artifacts":
                                ml_artifacts.append(full_path)
                            if category == "source_code":
                                source_code_files.append(full_path)
                    except:
                        pass
        
        if current_found:
            found_files = list(set(current_found))
            break
            
    if not readme_content and not found_files:
        raise HTTPException(status_code=404, detail="Repository not found or lacks a README. Spartans don't audit ghosts.")
        
    return {
        "found_files": found_files,
        "readme_content": readme_content,
        "tech_stack": tech_stack,
        "ml_artifacts": ml_artifacts,
        "source_code_files": source_code_files
    }
