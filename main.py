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


async def pato(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gets a duck from the web and replies it"""
    contents = requests.get("https://random-d.uk/api/v2/random").json()
    url = contents["url"]
    await update.message.reply_photo(url)


async def poketipo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Selects a random image from the folder and sends it to the user."""
    # Ensure the directory exists
    if not os.path.exists(IMAGE_FOLDER):
        await update.message.reply_text(
            f"Error: The directory '{IMAGE_FOLDER}' does not exist on the server."
        )
        return

    # List all files in the folder that match valid image extensions
    all_files = os.listdir(IMAGE_FOLDER)
    images = [f for f in all_files if f.lower().endswith(VALID_EXTENSIONS)]

    if not images:
        await update.message.reply_text("No supported images found in the folder.")
        return

    # Pick a random image filename
    random_image_name = random.choice(images)
    # Construct the full path to the image
    image_path = os.path.join(IMAGE_FOLDER, random_image_name)

    try:
        # Use 'send_document' instead of 'send_photo'
        with open(image_path, "rb") as document_file:
            await update.message.reply_document(
                document=document_file,
                filename=random_image_name,  # Keeps the exact original filename and extension
                caption=f"Here is your raw file: {random_image_name}",
            )
    except Exception as e:
        await update.message.reply_text(f"Failed to send file. Error: {e}")


if __name__ == "__main__":
    application = ApplicationBuilder().token(api_key).build()

    application.add_handler(CommandHandler("pato", pato))
    application.add_handler(CommandHandler("poketipo", poketipo))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    application.run_polling()
