from pathlib import Path

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
)


async def command_infobot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    version = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip().replace(".", r"\.")
    text = f"""***CAPI BOT***
***Versão do bot***: {version} \n
Feito com amor pela equipe dos Capivaras Mineiras <3"""

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.message.id,
        parse_mode=ParseMode.MARKDOWN_V2
    )
