
import requests

from telegram import Update
from telegram.ext import (
    ContextTypes,
)

async def command_pato(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gets a duck from the web and replies it"""
    contents = requests.get("https://random-d.uk/api/v2/random").json()
    url = contents["url"]
    await update.message.reply_photo(url)
