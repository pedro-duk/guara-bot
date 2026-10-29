import os
import random

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

import requests
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Specify the path to your folder containing images
# You can use relative paths like "./my_images" or absolute paths
IMAGE_FOLDER = "./assets/poketipo-stickers"

# Supported image extensions
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

STICKER_PACK_NAME = "PokemoodType"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def send_random_sticker(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Fetch the predetermined pack and reply with a random sticker from it."""
    try:
        # 1. Fetch the entire sticker set from Telegram's servers
        sticker_set = await context.bot.get_sticker_set(name=STICKER_PACK_NAME)

        # 2. Extract the list of sticker objects from the set
        stickers = sticker_set.stickers

        if not stickers:
            await update.message.reply_text("This sticker pack seems to be empty!")
            return

        # 3. Pick a random sticker from the sequence
        chosen_sticker_1 = random.choice(stickers)
        chosen_sticker_2 = random.choice(stickers)

        # 4. Reply directly using the sticker's unique file_id
        await update.message.reply_sticker(sticker=chosen_sticker_1.file_id)
        await update.message.reply_sticker(sticker=chosen_sticker_2.file_id)

    except Exception as e:
        logging.error(f"Error fetching or sending sticker: {e}")
        await update.message.reply_text(
            "Sorry, I couldn't fetch the sticker pack right now."
        )


if __name__ == "__main__":
    application = ApplicationBuilder().token(api_key).build()

    application.add_handler(CommandHandler("send_random_sticker", send_random_sticker))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    application.run_polling()
