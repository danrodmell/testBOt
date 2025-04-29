import os
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

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000/question")
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

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
        statements = result["statements"]
        return {"statements": statements, "answer_index": result["answer_index"]}
    except Exception as e:
        logging.error(f"Error connecting to backend: {e}")
        return None

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to Kruger Bot! Type /play to start a new game.")

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
        return
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
