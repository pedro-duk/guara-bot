from pathlib import Path

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
)


async def command_infouser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id_usuario = update.message.from_user.id

    text = f"""***INFORMAÇÕES DO SEU USUÁRIO***
***Seu id***: {id_usuario}"""

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.message.id,
        parse_mode=ParseMode.MARKDOWN_V2
    )
