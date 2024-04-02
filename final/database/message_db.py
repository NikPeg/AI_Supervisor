import datetime

import config
from . import database, cursor
from .session_db import get_user_session_id


def add_new_message(user_id, user_req, bot_req):
    session_id = get_user_session_id(user_id)
    date = datetime.datetime.now()
    cursor.execute("INSERT INTO Message VALUES(?,?,?,?,?)", (user_id, user_req, bot_req, session_id, date,))
    database.commit()


def get_conversation_by_user(user_id):
    print("!!!get_conversation_by_user")
    session_id = get_user_session_id(user_id)
    cursor.execute("SELECT * FROM Message WHERE user_id=? AND session_id=?", (user_id, session_id,))
    res = cursor.fetchone()
    print(f"SELECT * FROM Message WHERE user_id={user_id} AND session_id={session_id}")
    print(config.ADMIN_ID, res)
