import os
import logging

# Não mude isso - deve acontecer antes de chamar as calls do telegram
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# Importações de comandos
from commands.pato import command_pato
from commands.poketipo import command_poketipo
from commands.infobot import command_infobot
from commands.infouser import command_infouser

# Carregar env (só necessário para rodar localmente, mas não afeta a run na AWS)
load_dotenv(override=True)
api_key = os.getenv("API_KEY")

# Logging
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
    application.add_handler(CommandHandler("infobot", command_infobot))
    application.add_handler(CommandHandler("infouser", command_infouser))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command_echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)