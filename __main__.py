import os

import openai
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from dotenv import load_dotenv

load_dotenv()


openai.api_key = os.getenv('OPENAI_API')


def answer_question(question):
    """
    Use the OpenAI API to generate an answer to the given question
    """
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=question, max_tokens=256)
    answer = response.choices[0].text
    return answer


async def start(update, context):
    start_message = 'Hello! I\'m a bot for asking questions to ChatGPT3 ' \
        'directly in Telegram'
    await update.message.reply_text(start_message)


async def question(update, context):
    """
    Handle messages that contain a question
    """
    question = update.message.text
    answer = answer_question(question)
    await update.message.reply_text(answer)


def main() -> None:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN) \
        .read_timeout(30).write_timeout(30) \
        .build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, question))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
