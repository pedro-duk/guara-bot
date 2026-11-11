import os
import logging

# Don't change this - needs to be before telegram calls
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Command imports
from commands.pato import command_pato
from commands.poketipo import command_poketipo

# Load environment variables (only needed for local run but doesn't affect the amazon deploy)
load_dotenv(override=True)
api_key = os.getenv("API_KEY")

# Set logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def command_echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text("Olá! Digite / para ver a minha lista de comandos.")

if __name__ == "__main__":
    application = ApplicationBuilder().token(api_key).build()

    # Registering the commands
    application.add_handler(CommandHandler("pato", command_pato))
    application.add_handler(CommandHandler("poketipo", command_poketipo))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command_echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)