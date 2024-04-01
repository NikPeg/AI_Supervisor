import datetime

from . import database, cursor
from .sessia_db import get_user_session_id


def add_new_message(user_id, user_req, bot_req):
    session_id = get_user_session_id(user_id)
    date = datetime.datetime.now()
    cursor.execute("INSERT INTO Message VALUES(?,?,?,?,?)", (user_id, user_req, bot_req, session_id, date,))
    database.commit()
