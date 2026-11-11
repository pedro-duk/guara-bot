import os
import random
from io import BytesIO
from classes.user import User

from PIL import Image

# Don't change this - needs to be before telegram calls
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ContextTypes,
)

from utils.mongodb import *

from datetime import date

# Path to folder with images
IMAGE_FOLDER = "./assets/poketipo-images/WEBP"

# Supported image extensions
VALID_EXTENSIONS = ".webp"


# Gera os poketipos aleatórios a partir das imagens que já existem na pasta webp
def generate_poketipos():
    # Ensure the directory exists
    if not os.path.exists(IMAGE_FOLDER):
        logging.error("Generate_poketipos: diretório não existe")
        return None

    # List all files in the folder that match valid image extensions
    all_files = os.listdir(IMAGE_FOLDER)
    images = [f for f in all_files if f.lower().endswith(VALID_EXTENSIONS)]

    if not images:
        logging.error("Generate_poketipos: Não encontrou imagens")
        return None

    # Pick a random image filename
    random_image_name_1 = random.choice(images)
    random_image_name_2 = random.choice(images)

    # Construct the full path to the image
    image_path_1 = os.path.join(IMAGE_FOLDER, random_image_name_1)
    image_path_2 = os.path.join(IMAGE_FOLDER, random_image_name_2)

    return image_path_1, image_path_2


async def command_poketipo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Achar os dados usuário (comando cria novo se não tiver um)
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    user_data = find_user(user_name=user_name, user_id_to_search=user_id)

    if not user_data:
        await update.message.reply_text(
            "ERRO: Não foi encontrado usuário (checar logs)."
        )
        return

    # Verificar se usuário já fez poketipo HOJE
    is_today = user_data["timestamp_poketipo"].date() == date.today()

    if not is_today:
        # Gerar tipos e atualizar
        poketipo_path_1, poketipo_path_2 = generate_poketipos()

        if not poketipo_path_1:
            await update.message.reply_text(
                "ERRO: Não foi encontrado imagens (checar logs)."
            )
            return

        user_data["poketipo_path_1"] = poketipo_path_1
        user_data["poketipo_path_2"] = poketipo_path_2
        user_data["timestamp_poketipo"] = datetime.datetime.now()

        update_user(user_data)
    else:
        # Pegar tipos já definidos
        poketipo_path_1 = user_data["poketipo_path_1"]
        poketipo_path_2 = user_data["poketipo_path_2"]

    # Enviar mensagem inicial
    start_msg_text = (
        "Seus poketipos já foram gerados hoje. Aqui estão eles:"
        if is_today
        else f"Gerando os poketipos de {update.message.from_user.name}:"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_msg_text,
        reply_to_message_id=update.message.id,
    )

    try:
        # Enviar ambos poketipos
        for image_path in (poketipo_path_1, poketipo_path_2):
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=image_path,
                reply_to_message_id=update.message.id,
            )
    except Exception as e:
        await update.message.reply_text(f"Failed to send file. Error: {e}")
