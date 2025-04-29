# Deploying the Kruger Trivia Bot & Backend (Last Working Version)

This guide provides the simplest, most robust step-by-step instructions to deploy both the backend (FastAPI) and the Telegram bot. It is designed for reliability and minimal surprises.

---

## 1. **Prepare Your Project**
- Ensure your code is in a clean directory (e.g., `NewFolder`) with these files:
  - `backend.py` (FastAPI backend)
  - `bot.py` (Telegram bot)
  - `requirements_backend_bot.txt` (all dependencies)

---

## 2. **Deploying the Backend (FastAPI)**

### **Option A: Deploy on Render.com (Recommended for Simplicity)**
1. **Create a new web service** at [https://dashboard.render.com/](https://dashboard.render.com/)
2. **Connect your GitHub repo** containing `backend.py` and `requirements_backend_bot.txt`.
3. **Set build and start commands:**
   - **Build Command:**
     ```
     pip install -r requirements_backend_bot.txt
     ```
   - **Start Command:**
     ```
     uvicorn backend:app --host 0.0.0.0 --port 10000
     ```
4. **Set environment variables** (if needed).
5. **Deploy!**
6. **Test your endpoint:**  
   Visit `https://<your-app-name>.onrender.com/question` in your browser.

### **Option B: Deploy on Replit (for quick testing)**
- Upload your files to a new Python Repl.
- In the shell, run:
  ```
  pip install -r requirements_backend_bot.txt
  uvicorn backend:app --host 0.0.0.0 --port 10000
  ```
- Use the provided public URL for your bot.

---

## 3. **Deploying the Telegram Bot**

### **Recommended: Run on Your Own Server or a Cloud VM**
1. **Set your Telegram bot token as an environment variable:**
   ```
   export TELEGRAM_BOT_TOKEN=your_token_here
   export BACKEND_URL=https://<your-backend-url>/question
   ```
2. **Install dependencies:**
   ```
   pip install -r requirements_backend_bot.txt
   ```
3. **Run the bot:**
   ```
   python bot.py
   ```
- The bot will connect to your backend and be available on Telegram.

### **Notes:**
- If you want your bot to run 24/7, use a cloud VM (AWS Lightsail, DigitalOcean, etc.) or a Render background worker.
- Make sure your backend URL is public and reachable by the bot.

---

## 4. **Troubleshooting**
- If you see errors about missing packages, always run:
  ```
  pip install -r requirements_backend_bot.txt
  ```
- If you see import errors, try using a clean virtual environment.
- If the bot can't reach the backend, check your backend's public URL and firewall settings.

---

## 5. **Best Practices**
- Always use a requirements file dedicated to this project.
- Use environment variables for secrets (never hardcode tokens).
- Test both backend and bot locally before deploying.
- Document any changes or deployment steps for future reference.

---

**For improvements or production scaling, consider Dockerizing, using CI/CD, and adding logging/monitoring.**
