import datetime

from . import database, cursor
from .feedback_db import add_in_feedback_users


def add_new_user(user_id, username):
    check_ = check_user_status(user_id)
    if not check_:
        cursor.execute("INSERT INTO User(id, name) VALUES(?,?,?)", (user_id, username))
        database.commit()
        add_in_feedback_users(user_id)


def check_user_status(user_id):
    cursor.execute("SELECT id FROM User WHERE id=?", (user_id,))
    user_ = cursor.fetchone()
    if user_ is None:
        return False
    return True
