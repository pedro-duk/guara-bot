import os
import random
import requests
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
load_dotenv()
api_key = os.getenv("API_KEY")

# Set logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    application = ApplicationBuilder().token(api_key).build()

    # Registering the commands
    application.add_handler(CommandHandler("pato", command_pato))
    application.add_handler(CommandHandler("poketipo", command_poketipo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)