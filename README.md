# KrugerBot Trivia Backend

Welcome to the **KrugerBot FastAPI Backend** repository! This project powers the backend for the "Two Truths and a Twist" trivia game, integrated with a Telegram bot and designed for rapid, collaborative, and scalable development using AI copilots.

---

## 🚀 Project Overview
- **Backend:** FastAPI (Python)
- **Purpose:** Serve dynamic trivia questions (with a "twist") for the Telegram game bot.
- **Integrations:** OSO API (for open-source project data), Telegram Bot API
- **Deployment:** Designed for cloud platforms (Render.com recommended for Python APIs)

---

## 🏆 Best Practices & Copilot Collaboration

This repo is a **living guide for best practices when working with AI copilots** (like Cascade, GitHub Copilot, ChatGPT, etc):

### 1. **Clarity & Documentation**
- Always document major design decisions, environment variables, and API integrations in the README.
- Maintain a clear and up-to-date `requirements.txt` and `Procfile` for easy deployment.
- Use `.gitignore` to keep sensitive and unnecessary files out of source control.

### 2. **Environment Management**
- Use a dedicated virtual environment for each project to avoid dependency conflicts (especially with packages like `rich` and `streamlit`).
- Store all sensitive keys (API keys, tokens) as environment variables, never in code.

### 3. **Rapid Iteration, Safe Deployment**
- For MVPs, prioritize speed, but always keep a record of known risks and trade-offs.
- Use free-tier cloud platforms (Render, Railway, etc.) for fast, scalable deployment.
- If a platform is not suited for your stack (e.g., Netlify for Python APIs), switch quickly to a better fit.

### 4. **Copilot Collaboration**
- Treat your AI copilot as a pair programmer: be explicit about goals, blockers, and desired workflow.
- Ask for best-practice suggestions and request living documentation updates as you go.
- Review all copilot code changes before deploying to production.

### 5. **Error Handling & Debugging**
- Always check cloud logs for deployment errors (missing env vars, build failures, etc.).
- Test your endpoints directly (e.g., `/question`) before connecting to clients (Telegram, frontend, etc.).
- Add defensive checks in code to avoid API errors or missing data.

### 6. **Onboarding & Handover**
- Keep this README and a `MVP_Roadmap.md` up to date for new contributors.
- Summarize major architectural decisions and lessons learned.

---

## ⚡️ Quickstart

1. **Clone the repo:**
   ```sh
   git clone https://github.com/danrodmell/TGBOT.git
   cd TGBOT
   ```
2. **Create a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set environment variables:**
   - `OSO_API_KEY` (get from OSO)
5. **Run locally:**
   ```sh
   uvicorn oso_trivia_backend:app --reload
   ```
6. **Deploy:**
   - Use Render.com or Railway for cloud deployment.

---

## 🤖 Telegram Bot Integration
- Update the `BACKEND_URL` in your `telegram_bot.py` to point to your deployed backend.
- The bot will fetch questions from `/question` endpoint.

---

## 📚 Living Best Practices
- Update this README as new insights, workflow improvements, or onboarding tips are discovered.
- If you encounter a blocker, document the root cause and solution here for future teams.

---

## 🙏 Credits & Acknowledgments
- Built by Daniel Melendez and Cascade Copilot, 2025.
- Inspired by the open-source and AI developer communities.

---

*“The more we learn, the less we know.” — KrugerBot*
