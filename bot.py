import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from rag.generate import answer_question

# Load env variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Ask me anything."
    )


# Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text

    await update.message.reply_text("Thinking...")

    answer = answer_question(user_question)

    await update.message.reply_text(answer)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()