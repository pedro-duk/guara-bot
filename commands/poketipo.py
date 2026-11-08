
import os
import random

# Don't change this - needs to be before telegram calls
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ContextTypes,
)

# Path to folder with images
IMAGE_FOLDER = "./assets/poketipo-images"

# Supported image extensions
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")

async def command_poketipo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    random_image_name_1 = random.choice(images)
    random_image_name_2 = random.choice(images)
    # Construct the full path to the image
    image_path_1 = os.path.join(IMAGE_FOLDER, random_image_name_1)
    image_path_2 = os.path.join(IMAGE_FOLDER, random_image_name_2)


    try:
        # Send the document as a raw webp, making it LOOK like a sticker!
        with open(image_path_1, "rb") as document_file:
            await update.message.reply_document(
                document=document_file,
                filename=random_image_name_1,  # Keeps the exact original filename and extension
                caption=f"Here is your raw file: {random_image_name_1}",
            )

        # Send the second image!
        with open(image_path_2, "rb") as document_file:
            await update.message.reply_document(
                document=document_file,
                filename=random_image_name_2,  # Keeps the exact original filename and extension
                caption=f"Here is your raw file: {random_image_name_2}",
            )
    except Exception as e:
        await update.message.reply_text(f"Failed to send file. Error: {e}")

