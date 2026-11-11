from classes.user import User
from utils.mongodb import *

from telegram import Update
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import (
    ContextTypes,
)


async def command_infouser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.message.from_user.name
    user_id = update.message.from_user.id

    user_data = find_user(user_name=user_name, user_id_to_search=user_id)

    text = f"""*INFORMAÇÕES DO SEU USUÁRIO*
*Seu id*: {user_id}
*Último poketipo*: {escape_markdown(user_data["timestamp_poketipo"].strftime("%d/%m/%Y"), version=2)}"""

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.message.id,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
