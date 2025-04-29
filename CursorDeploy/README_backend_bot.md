# Kruger Trivia Bot & Backend (Last Working Version)

This folder contains the last working, minimal, and robust implementation of both the trivia backend and Telegram bot.

## Files
- `backend.py`: FastAPI backend serving `/question` endpoint with simple "which is NOT a real project" logic.
- `bot.py`: Telegram bot that connects to the backend, asks questions, and tracks user score/streak.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements_backend_bot.txt
```

### 2. Run the backend
```bash
uvicorn backend:app --reload
```
- The backend will be available at http://localhost:8000/question

### 3. Set your Telegram bot token
```bash
export TELEGRAM_BOT_TOKEN=your_token_here
```

### 4. Run the bot
```bash
python bot.py
```

## Usage
- Start a conversation with your Telegram bot and type `/play` to begin.
- The bot will fetch questions from the backend and handle scoring and streaks.

---
This version is intended for easy redeployment and debugging. For any issues, rollback to this state.
