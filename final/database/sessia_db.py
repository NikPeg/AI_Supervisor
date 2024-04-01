import datetime

from loader import database, cursor


def get_user_session_id(user_id):
    cursor.execute("SELECT id FROM Session WHERE user_id=?", (user_id,))
    session_id = cursor.fetchone()
    if session_id is None:
        return int(0)
    return int(session_id[0])


def create_new_session(user_id):
    session_id = get_user_session_id(user_id)
    session_id += int(1)
    date = datetime.datetime.now()
    cursor.execute("INSERT INTO Session VALUES(?,?,?)", (user_id, session_id, date,))
    database.commit()
