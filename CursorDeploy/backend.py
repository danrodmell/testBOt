from fastapi import FastAPI
import random
import re

app = FastAPI()

# --- Fallback question bank ---
FALLBACK_QUESTIONS = [
    {
        "statements": [
            "'bertyX' is a real open source project.",
            "'hubbleprotocol' is a real open source project.",
            "'heineiuo' is a real open source project."
        ],
        "answer_index": 0
    },
    {
        "statements": [
            "'0xb7b2e53a325bf3cc1e42d2b24e485f2e699fbb390c656ba9ffe3d8162a875561' is a real open source project.",
            "'0xb7b2e53a325bf3cc1e42d2b24e485f2e699fbb390c656ba9ffe3d8162a875561X' is a real open source project.",
            "'0x69526c6276b49a35d788e6c13d16b3bab6d1501908926364176ffa4400479cb4' is a real open source project."
        ],
        "answer_index": 1
    }
]

# --- Simple, robust question generator ---
def generate_trivia():
    # For demo: use static fallback logic. In production, replace with DB/API logic.
    try:
        # Simulate a list of real project names
        projects = [
            'hubbleprotocol', 'heineiuo', 'bertyX',
            '0xb7b2e53a325bf3cc1e42d2b24e485f2e699fbb390c656ba9ffe3d8162a875561',
            '0x69526c6276b49a35d788e6c13d16b3bab6d1501908926364176ffa4400479cb4'
        ]
        def is_human(name):
            if not isinstance(name, str): return False
            if re.fullmatch(r"0x[a-fA-F0-9]{10,}", name): return False
            if len(name) < 3 or len(name) > 40: return False
            if not re.search(r"[a-zA-Z]", name): return False
            if name.lower() in ("unknown", "n/a", "none", "null"): return False
            return True
        real = [p for p in projects if is_human(p)]
        wallets = [p for p in projects if not is_human(p)]
        if len(real) < 2 or len(wallets) < 1:
            raise ValueError("Not enough data to generate question.")
        selected_real = random.sample(real, 2)
        selected_wallet = random.choice(wallets)
        options = selected_real + [selected_wallet]
        random.shuffle(options)
        answer_index = options.index(selected_wallet)
        statements = [f"'{opt}' is a real open source project." for opt in options]
        return {
            "statements": statements,
            "answer_index": answer_index
        }
    except Exception as e:
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
        return {"error": str(e)}
