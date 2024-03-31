import datetime

from . import database, cursor
from .feedback_db import add_in_feedback_users


def add_new_user(user_id, user_nick):
    if not check_user_status(user_id):
        date = datetime.datetime.now()
        cursor.execute("INSERT INTO Users VALUES(?,?,?)", (user_id, f"@{user_nick}", date,))
        database.commit()
        add_in_feedback_users(user_id)


def check_user_status(user_id):
    cursor.execute("SELECT user_id FROM Users WHERE user_id=?", (user_id,))
    if cursor.fetchone() is None:
        return False
    return True
