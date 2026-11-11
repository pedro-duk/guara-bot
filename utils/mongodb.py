import os
import logging
import datetime
from pymongo import MongoClient
from classes.user import User

mongodb_uri = os.getenv("MONGODB_KEY")
database_name = os.getenv("DATABASE_NAME")
users_collection_name = os.getenv("USERS_COLLECTION_NAME")


def connect_mongodb():
    global client
    global database
    global users_collection

    client = MongoClient(mongodb_uri)
    try:
        client.admin.command("ping")
        print("Connected successfully")
    except Exception as e:
        logging.error("The following error occurred: ", e)

    database = client[database_name]
    users_collection = database[users_collection_name]


def test_connection():
    try:
        client.admin.command("ping")
        print("Connected successfully")
    except Exception as e:
        connect_mongodb()


def insert_user(user_to_insert: User):
    test_connection()

    try:
        users_collection.insert_one(user_to_insert)
    except Exception as e:
        logging.error("The following error occurred: ", e)


def update_user(user_to_update: User):
    test_connection()

    try:
        user_data = (
            vars(user_to_update)
            if hasattr(user_to_update, "__dict__")
            else dict(user_to_update)
        )
        users_collection.update_one(
            {"telegram_id": user_to_update["telegram_id"]},
            {"$set": user_data},
        )
    except Exception as e:
        logging.error("The following error occurred: %s", e)


def find_user(user_name: str, user_id_to_search: int):
    user_id_to_search = str(user_id_to_search)
    test_connection()

    try:
        found_user = users_collection.find_one(User(telegram_id=user_id_to_search))

        if not found_user:
            found_user = User(
                name=user_name,
                telegram_id=user_id_to_search,
                timestamp_poketipo=datetime.datetime.now() - datetime.timedelta(days=7),
                poketipo_path_1="",
                poketipo_path_2="",
            )
            insert_user(found_user)

        return found_user
    except Exception as e:
        logging.error("The following error occurred: ", e)
