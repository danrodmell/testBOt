import os
import sys
import logging
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

CHOOSING, ANSWERING = range(2)
user_sessions = {}

BACKEND_URL = os.environ.get("KRUGER_BACKEND_URL", "https://kruger-trivia-backend.onrender.com/question")
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

WELCOME_MESSAGE = (
    "Welcome to Kruger Bot!\n\nGame Rules:\n"
    "You’ll be presented with three statements: two are true, one is a twist (a false or misleading fact). "
    "Your goal is to spot the twist! Score points for correct answers and build your streak for bonus multipliers."
    "\nType /play to start."
)

FALLBACK_QUESTIONS = [
    {
        "statements": [
            "The Eiffel Tower is in Paris.",
            "The Great Wall of China is visible from space.",
            "Mount Everest is the tallest mountain on Earth."
        ],
        "answer_index": 1
    },
    {
        "statements": [
            "Sharks are mammals.",
            "The Pacific Ocean is the largest ocean on Earth.",
            "Venus is the closest planet to the Sun."
        ],
        "answer_index": 0
    }
]

def fetch_backend_question():
    try:
        resp = requests.get(BACKEND_URL, timeout=5)
        if resp.status_code != 200:
            logging.error(f"Backend returned status {resp.status_code}: {resp.text}")
            return None
        result = resp.json()
        if not isinstance(result, dict) or "statements" not in result or "answer_index" not in result:
            logging.error(f"Malformed backend response: {result}")
            return None
        # Always coerce statements to list
        if isinstance(result["statements"], str):
            statements = [s.strip() for s in result["statements"].split("\n") if s.strip()]
        else:
            statements = result["statements"]
        return {"statements": statements, "answer_index": result["answer_index"]}
    except Exception as e:
        logging.error(f"Error connecting to backend: {e}")
        return None

def start(update: Update, context: CallbackContext):
    update.message.reply_text(WELCOME_MESSAGE)
    update.message.reply_text("Type /play to start a new game.")

def play(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    result = fetch_backend_question()
    if not result:
        result = random.choice(FALLBACK_QUESTIONS)
        update.message.reply_text("Backend is unavailable or returned bad data. Using a fallback question.")
    user_sessions[user_id] = {
        "current_result": result,
        "score": 0,
        "streak": 0,
    }
    send_question(update, context, result)
    return ANSWERING

def send_question(update, context, result):
    statements = result["statements"]
    keyboard = [[str(i+1)] for i in range(len(statements))]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    msg = "Spot the twist!\n\n"
    for i, st in enumerate(statements):
        msg += f"{i+1}. {st}\n"
    update.message.reply_text(msg, reply_markup=markup)

def answer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in user_sessions:
        update.message.reply_text("Please start a new game with /play.")
        return ConversationHandler.END
    session = user_sessions[user_id]
    try:
        idx = int(update.message.text.strip()) - 1
    except Exception:
        update.message.reply_text("Please reply with the number of your answer.")
        return ANSWERING
    correct = (idx == session["current_result"]["answer_index"])
    if correct:
        session["score"] += 1
        session["streak"] += 1
        msg = "Correct!\n"
    else:
        session["streak"] = 0
        msg = f"Twist! The correct answer was option {session['current_result']['answer_index']+1}.\n"
    msg += f"Score: {session['score']}\nStreak: {session['streak']}\n"
    # Next question
    next_result = fetch_backend_question()
    if not next_result:
        next_result = random.choice(FALLBACK_QUESTIONS)
        update.message.reply_text(msg + "\nBackend is unavailable or returned bad data. Using a fallback question.", reply_markup=ReplyKeyboardRemove())
        del user_sessions[user_id]
        return ConversationHandler.END
    session["current_result"] = next_result
    update.message.reply_text(msg)
    send_question(update, context, next_result)
    return ANSWERING

def cancel(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
    update.message.reply_text('Game cancelled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    global TOKEN
    if not TOKEN:
        TOKEN = input("Enter your Telegram bot token: ").strip()
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set and no token provided.")
        sys.exit(1)
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('play', play)],
        states={
            ANSWERING: [MessageHandler(Filters.text & ~Filters.command, answer)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('cancel', cancel))
    print("Kruger Bot is running. Press Ctrl+C to stop.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
