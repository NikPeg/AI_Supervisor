import sqlite3

from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

storage = MemoryStorage()

database = sqlite3.connect(config.DB_FILENAME)
cursor = database.cursor()
