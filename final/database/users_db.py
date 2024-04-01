import datetime

from loader import database, cursor
from .feedback_db import add_in_feedback_users


def add_new_user(user_id, user_nick):
    check_ = check_user_status(user_id)
    if not check_:
        date = datetime.datetime.now()
        cursor.execute("INSERT INTO User VALUES(?,?,?)", (user_id, f"@{user_nick}", date,))
        database.commit()
        add_in_feedback_users(user_id)


def check_user_status(user_id):
    cursor.execute("SELECT user_id FROM User WHERE user_id=?", (user_id,))
    user_ = cursor.fetchone()
    if user_ is None:
        return False
    return True
