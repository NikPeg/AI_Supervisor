from . import database, cursor
from .feedback_db import add_in_feedback_users
from datetime import datetime, timedelta


def add_new_user(user_id, username):
    check_ = check_user_status(user_id)
    if not check_:
        paid_by = datetime.now() + timedelta(days=2)
        cursor.execute("INSERT INTO User(id, name, paid_by) VALUES(?,?,?)", (user_id, username, paid_by))
        database.commit()
        add_in_feedback_users(user_id)


def check_user_status(user_id):
    cursor.execute("SELECT id FROM User WHERE id=?", (user_id,))
    user_ = cursor.fetchone()
    if user_ is None:
        return False
    return True


def get_all_users():
    cursor.execute("SELECT id, name FROM User")
    all_users = cursor.fetchall()
    return all_users
