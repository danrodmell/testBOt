from fastapi import FastAPI
from pyoso.client import Client
import os
import random
import re

app = FastAPI()

# Initialize OSO Client
API_KEY = os.environ.get("OSO_API_KEY")
oso_client = Client(api_key=API_KEY)

def get_human_projects(n=10):
    df = oso_client.to_pandas("SELECT project_name FROM projects_v1 LIMIT 200")
    # Filter out names that look like wallet addresses or hashes
    def is_human(name):
        if not isinstance(name, str): return False
        if re.fullmatch(r"0x[a-fA-F0-9]{10,}", name): return False
        if len(name) < 3 or len(name) > 40: return False
        if not re.search(r"[a-zA-Z]", name): return False
        if name.lower() in ("unknown", "n/a", "none", "null"): return False
        return True
    projects = [p for p in df["project_name"].dropna().unique() if is_human(p)]
    if len(projects) < n:
        return None
    return random.sample(projects, n)

# New: Get project stars

def get_project_stars():
    df = oso_client.to_pandas("SELECT project_name, stars FROM key_metrics_by_project_v0 WHERE stars IS NOT NULL ORDER BY stars DESC LIMIT 20")
    df = df[df["project_name"].apply(lambda n: isinstance(n, str) and len(n) < 40 and not n.startswith('0x'))]
    return df.to_dict(orient="records")

# New: Get project contributors

def get_project_contributors():
    df = oso_client.to_pandas("SELECT project_name, contributors FROM key_metrics_by_project_v0 WHERE contributors IS NOT NULL ORDER BY contributors DESC LIMIT 20")
    df = df[df["project_name"].apply(lambda n: isinstance(n, str) and len(n) < 40 and not n.startswith('0x'))]
    return df.to_dict(orient="records")

def get_key_metrics():
    # Defensive: Only proceed if 'key_metrics_by_project_v0' has a usable column
    try:
        df = oso_client.to_pandas("SELECT * FROM key_metrics_by_project_v0 LIMIT 1")
        # Try to find a metric-like column
        for col in df.columns:
            if col not in ("project_name", "id") and df[col].dtype in [int, float]:
                return [col]
        # Fallback: no usable metric columns
        return []
    except Exception:
        return []

def get_contract_names():
    # Disabled due to OSO schema change: contract_name column not found
    return []

def get_security_libs():
    df = oso_client.to_pandas("SELECT DISTINCT project_name FROM projects_v1 WHERE LOWER(project_name) LIKE '%security%' OR LOWER(project_name) LIKE '%audit%' OR LOWER(project_name) LIKE '%safe%' LIMIT 100")
    libs = [l for l in df["project_name"].dropna().unique() if isinstance(l, str) and len(l) < 40]
    return libs

def format_statements(statements):
    return [f"{i+1}. {s}" for i, s in enumerate(statements)]

def make_fake(name):
    # Make a more natural fake
    base = name.split()[0][:20]
    return base + random.choice(["-Fake", "-NotAProject", "-Twist", "_X"])

def truncate_name(name, maxlen=25):
    return name if len(name) <= maxlen else name[:maxlen-3] + "..."

# Only use columns verified from OSO schema probe
# artifacts_v1: ['artifact_id', 'artifact_source_id', 'artifact_source', 'artifact_namespace', 'artifact_name']
# projects_v1: ['project_id', 'project_source', 'project_namespace', 'project_name', 'display_name', 'description']

import random

# --- Fallback question bank ---
FALLBACK_QUESTIONS = [
    {
        "intro": "🌟 Ready for a challenge? Here are three project names. One of them is a clever fake! Can you spot the twist?",
        "statements": "1. 'OpenAI GPT' is a real open source project.\n2. 'TensorFlow' is a real open source project.\n3. 'QuantumBanana' is a real open source project.",
        "answer_index": 2,
        "options": ["OpenAI GPT", "TensorFlow", "QuantumBanana"],
        "twist": "QuantumBanana",
        "outro": "Reply with the number you think is the twist!"
    },
    {
        "intro": "🧩 Which of these is NOT a real open source artifact? Find the twist!",
        "statements": "1. 'NumPy' is a real open source artifact.\n2. 'PyTorch' is a real open source artifact.\n3. 'BananaTorch' is a real open source artifact.",
        "answer_index": 2,
        "options": ["NumPy", "PyTorch", "BananaTorch"],
        "twist": "BananaTorch",
        "outro": "Reply with the number you think is the twist!"
    },
]

# --- MCP-style, human-centric question generator ---
def generate_trivia():
    # Choose a question type that is human-friendly and based on verified columns
    qtypes = ["project_display", "artifact_name"]
    qtype = random.choice(qtypes)
    try:
        if qtype == "project_display":
            df = oso_client.to_pandas("SELECT DISTINCT display_name FROM projects_v1 WHERE display_name IS NOT NULL LIMIT 20")
            names = [n for n in df["display_name"].dropna().unique() if isinstance(n, str) and len(n) < 40]
            if len(names) < 3:
                raise ValueError("Not enough project names to generate question.")
            choices = random.sample(names, 3)
            twist = make_fake(choices[0])
            twist_index = random.randint(0, 2)
            statements = [f"{i+1}. '{c}' is a real open source project." for i, c in enumerate(choices)]
            statements[twist_index] = f"{twist_index+1}. '{twist}' is a real open source project."
            return {
                "intro": "🌟 Ready for a challenge? Here are three project names. One of them is a clever fake! Can you spot the twist?",
                "statements": "\n".join(statements),
                "answer_index": twist_index,
                "options": choices + [twist],
                "twist": twist,
                "outro": "Reply with the number you think is the twist!"
            }
        elif qtype == "artifact_name":
            df = oso_client.to_pandas("SELECT DISTINCT artifact_name FROM artifacts_v1 WHERE artifact_name IS NOT NULL LIMIT 20")
            names = [n for n in df["artifact_name"].dropna().unique() if isinstance(n, str) and len(n) < 40]
            if len(names) < 3:
                raise ValueError("Not enough artifact names to generate question.")
            choices = random.sample(names, 3)
            twist = make_fake(choices[0])
            twist_index = random.randint(0, 2)
            statements = [f"{i+1}. '{c}' is a real open source artifact." for i, c in enumerate(choices)]
            statements[twist_index] = f"{twist_index+1}. '{twist}' is a real open source artifact."
            return {
                "intro": "🧩 Which of these is NOT a real open source artifact? Find the twist!",
                "statements": "\n".join(statements),
                "answer_index": twist_index,
                "options": choices + [twist],
                "twist": twist,
                "outro": "Reply with the number you think is the twist!"
            }
        else:
            raise ValueError("No valid question types available.")
    except Exception as e:
        # Fallback to local questions
        fallback = random.choice(FALLBACK_QUESTIONS)
        return fallback

@app.get("/question")
def get_question():
    try:
        trivia = generate_trivia()
        if trivia is None:
            return {"error": "Not enough data to generate question."}
        return trivia
    except Exception as e:
        print("ERROR in /question:", e)
        return {"error": str(e)}
