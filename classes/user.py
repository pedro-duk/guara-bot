from typing import TypedDict
from datetime import datetime

class User(TypedDict):
    name: str
    telegram_id: str
    timestamp_poketipo: datetime
    poketipo_path_1: str
    poketipo_path_2: str