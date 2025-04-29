# MCP Project: Junior Developer User Manual (Windsurf + Copilot)

---

## 1. Project Overview
- **Goal:** Build a simple trivia game backend (FastAPI) and Telegram bot, deployed via Windsurf.
- **Why:** Learn modular development, deployment, and integration using modern tools.
- **Reference Repo:** https://github.com/tiangolo/fastapi (FastAPI examples)

---

## 2. Architecture Diagram
```
+-------------------+         REST API         +----------------------+
|   Telegram Bot    | <---------------------> |   FastAPI Backend    |
+-------------------+                         +----------------------+
        |                                              |
        v                                              v
+---------------------------------------------------------------+
|                        Windsurf Infra/Cloud                   |
+---------------------------------------------------------------+
```

---

## 3. Modular Roadmap (with Estimated Hours)

Milestone,Job to Be Done,Tool(s),Estimated Hours,Summary/Instructions
Project Kickoff,Understand project goals and requirements,Windsurf,1,Read this manual and clarify requirements with your PM.
Infra Setup,Scaffold backend infra (dev/staging),Windsurf,2,Use Windsurf templates to set up FastAPI backend infra.
Environment Setup,Configure environment variables,Windsurf,1,Follow Windsurf prompts to set DB_URL, SECRET_KEY, etc.
API Scaffolding,Generate basic FastAPI endpoints (e.g., /question),Copilot (Cascade, Cursor, Gemini),2,Prompt Copilot to generate endpoint code and OpenAPI spec.
Bot Integration,Integrate Telegram bot with backend,Copilot,2,Use Copilot to scaffold bot logic and connect to FastAPI.
Testing,Write and run basic tests for endpoints and bot,Copilot,2,Prompt Copilot to generate tests; run with pytest.
Deployment,Automate deployment to staging,Windsurf,2,Use Windsurf one-click deploy to cloud/staging.
Monitoring,Set up basic monitoring and logging,Windsurf,1,Enable Prometheus/Grafana in Windsurf infra.
Documentation,Auto-generate and review docs,Copilot,1,Prompt Copilot to generate README and API docs.
Integration Check,Test end-to-end flow (bot <-> API <-> infra),Both,2,Follow checklist to verify integration at each step.

---

## 4. Documentation Template

### Project Overview
- What is the project and why does it matter?
- Who are the stakeholders?

### Architecture Diagram
- Visualize the main components and how they connect.

### Milestone Roadmap
- List each step, the job to be done, tool, and estimated time.

### Environment Variables (Schema)
Variable,Required,Description,Example Value
DB_URL,Yes,Database connection string,postgres://user:pass@host/db
SECRET_KEY,Yes,JWT signing key,supersecret123
API_URL,Yes,Backend API base URL,https://api.example.com
TELEGRAM_BOT_TOKEN,Yes,Telegram bot token,123456:ABC-DEF

### Step-by-Step Instructions
- For each milestone, read the summary and instructions.
- Use the recommended tool (Windsurf or Copilot).
- Test integration before moving to the next step.

### Testing & Integration Checklist
- [ ] FastAPI endpoint returns valid response
- [ ] Bot sends/receives messages via backend
- [ ] Deployment is successful (Windsurf)
- [ ] Monitoring/logging is active

### Troubleshooting
- If deployment fails, check Windsurf logs and environment variables.
- If bot is unresponsive, verify API_URL and token.
- Use public repos for reference: https://github.com/python-telegram-bot/python-telegram-bot

---

## 5. Schema Example (CSV)

Section,Name,Type/Method,Description,Example,Notes
API Endpoint,/question,GET,Get trivia question,GET /question,{"statements": [...], "answer_index": 2}
Backend Module,backend.py,Module,Serves trivia question,get_question,All logic in one file
Data Model,Question,statements,answer_index,Simple dict,{"statements": [...], "answer_index": 2}
Env Variable,TELEGRAM_BOT_TOKEN,String,Telegram bot token,123456:ABC-DEF,Required
Env Variable,BACKEND_URL,String,Backend API endpoint,https://backend.onrender.com/question,Required
Tool,FastAPI,Framework,Python web API framework,pip install fastapi,Backend
Tool,python-telegram-bot,Library,Telegram bot integration,pip install python-telegram-bot,Bot
Tool,requests,Library,HTTP requests,pip install requests,Bot
Tool,uvicorn,Server,ASGI server,uvicorn backend:app,Bot

---

## 6. Summary for the User
- Read each section before starting the task.
- Use Windsurf for infra and deployment, Copilot for code and docs.
- Always test after each milestone.
- Reference public repos for working examples.
- If stuck, ask for help early!

---

*This manual is designed for junior developers to ship modular tools step by step, with clear jobs to be done, documentation, and integration checks at every stage.*
