# Kruger Telegram Bot

A clean, production-ready Telegram bot for the Kruger trivia game, designed for reliability and maintainability.

## Features
- Fetches trivia questions from your backend (`/question` endpoint)
- Score saving and streak/bonus system (in memory for MVP)
- Graceful fallback questions if backend is unavailable
- MCP/OSO-style questions, no wallet/random nonsense
- Optimized for clarity and user experience

## Requirements
- Python 3.8+
- `python-telegram-bot==13.15`
- `requests`

## Setup
1. **Install dependencies**
   ```bash
   pip install python-telegram-bot==13.15 requests
   ```
2. **Set environment variables:**
   - `TELEGRAM_BOT_TOKEN` (your Telegram bot token)
   - `KRUGER_BACKEND_URL` (optional, defaults to Render deployment)

3. **Run the bot:**
   ```bash
   export TELEGRAM_BOT_TOKEN=YOUR_TOKEN_HERE
   python bot.py
   ```
   If you don't set the token as an environment variable, you'll be prompted for it at startup.

## Deployment
- For production, run with a process manager (e.g., systemd, pm2, or cloud service like Render).
- No hardcoded secrets; all config is via environment variables.

## Troubleshooting
- If the bot always uses fallback questions, check that your backend `/question` endpoint returns:
  ```json
  {
    "statements": ["...", "...", "..."],
    "answer_index": 1
  }
  ```
- For persistent score saving, integrate a database (future version).

---
**For any issues, check your backend API logs and ensure the bot can reach it from your server.**
