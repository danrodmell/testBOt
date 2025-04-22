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
    df = oso_client.to_pandas("SELECT DISTINCT contract_name FROM contracts_v0 LIMIT 100")
    contracts = [c for c in df["contract_name"].dropna().unique() if isinstance(c, str) and len(c) < 40 and not c.startswith('0x')]
    return contracts

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

# Generate a Two Truths and a Twist question using several templates

def generate_trivia():
    qtypes = ["project_name", "stars", "contributors", "contract", "security_lib"]
    metrics = get_key_metrics()
    if metrics:
        qtypes.append("metric")
    qtype = random.choice(qtypes)
    intro = "Spot the twist!"
    outro = "Pick the twist!"
    if qtype == "metric":
        if not metrics:
            qtype = "project_name"
        else:
            choices = [truncate_name(m) for m in random.sample(metrics, 1)]
            twist = random.choice(["Unicorn Power", "Quantum Speed", "AI Sentience", "Zero Trust Magic"])
            twist_index = 0
            statements = [f"'{c}' is a tracked key metric in OSO analytics." for c in choices]
            statements[twist_index] = f"'{twist}' is a tracked key metric in OSO analytics."
            return {
                "intro": intro,
                "statements": format_statements(statements),
                "answer_index": twist_index,
                "options": choices + [twist],
                "twist": twist,
                "outro": outro
            }
    if qtype == "contract":
        contracts = [truncate_name(c) for c in get_contract_names()]
        if not contracts or len(contracts) < 3:
            qtype = "project_name"
        else:
            choices = random.sample(contracts, 3)
            twist = make_fake(choices[0])
            twist_index = random.randint(0, 2)
            statements = [f"'{c}' is a deployed smart contract in the OSO data lake." for c in choices]
            statements[twist_index] = f"'{twist}' is a deployed smart contract in the OSO data lake."
            return {
                "intro": intro,
                "statements": format_statements(statements),
                "answer_index": twist_index,
                "options": choices + [twist],
                "twist": twist,
                "outro": outro
            }
    if qtype == "security_lib":
        libs = [truncate_name(l) for l in get_security_libs()]
        if not libs or len(libs) < 3:
            qtype = "project_name"
        else:
            choices = random.sample(libs, 3)
            twist = make_fake(choices[0])
            twist_index = random.randint(0, 2)
            statements = [f"'{c}' is an open source security library." for c in choices]
            statements[twist_index] = f"'{twist}' is an open source security library."
            return {
                "intro": intro,
                "statements": format_statements(statements),
                "answer_index": twist_index,
                "options": choices + [twist],
                "twist": twist,
                "outro": outro
            }
    if qtype == "stars":
        data = get_project_stars()
        if not data or len(data) < 3:
            qtype = "project_name"
        else:
            choices = random.sample(data, 3)
            choices = [{"project_name": truncate_name(c["project_name"]), "stars": c["stars"]} for c in choices]
            twist_index = random.randint(0, 2)
            twist = make_fake(choices[twist_index]["project_name"])
            statements = [
                f"'{c['project_name']}' has over {c['stars']} stars on GitHub." for c in choices
            ]
            statements[twist_index] = f"'{twist}' has over {choices[twist_index]['stars']} stars on GitHub."
            return {
                "intro": intro,
                "statements": format_statements(statements),
                "answer_index": twist_index,
                "options": [c['project_name'] for c in choices] + [twist],
                "twist": twist,
                "outro": outro
            }
    if qtype == "contributors":
        data = get_project_contributors()
        if not data or len(data) < 3:
            qtype = "project_name"
        else:
            choices = random.sample(data, 3)
            choices = [{"project_name": truncate_name(c["project_name"]), "contributors": c["contributors"]} for c in choices]
            twist_index = random.randint(0, 2)
            twist = make_fake(choices[twist_index]["project_name"])
            statements = [
                f"'{c['project_name']}' has over {c['contributors']} contributors." for c in choices
            ]
            statements[twist_index] = f"'{twist}' has over {choices[twist_index]['contributors']} contributors."
            return {
                "intro": intro,
                "statements": format_statements(statements),
                "answer_index": twist_index,
                "options": [c['project_name'] for c in choices] + [twist],
                "twist": twist,
                "outro": outro
            }
    # Default: project name only, but filtered
    projects = [truncate_name(p) for p in get_human_projects()]
    if not projects:
        return None
    twist = make_fake(projects[0])
    statements = [f"'{p}' is a real open source project." for p in projects[:3]]
    twist_index = random.randint(0, 2)
    statements[twist_index] = f"'{twist}' is a real open source project."
    return {
        "intro": intro,
        "statements": format_statements(statements),
        "answer_index": twist_index,
        "options": projects[:3] + [twist],
        "twist": twist,
        "outro": outro
    }

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
