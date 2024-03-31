import datetime

from . import database, cursor
from .sessia_db import get_user_sessia_id


def add_new_message(user_id, user_req, bot_req):
    sessia_id = get_user_sessia_id(user_id)
    date = datetime.datetime.now()
    cursor.execute("INSERT INTO All_messages VALUES(?,?,?,?,?)", (user_id, user_req, bot_req, sessia_id, date,))
    database.commit()
