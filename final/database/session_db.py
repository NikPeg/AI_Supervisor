from . import database, cursor


def create_new_session(user_id):
    cursor.execute("INSERT INTO Session(user_id) VALUES(?)", (user_id,))
    database.commit()
    cursor.execute("SELECT id FROM Session WHERE user_id=?", (user_id,))
    return int(cursor.fetchone()[0])


def get_user_session_id(user_id):
    cursor.execute("SELECT id FROM Session WHERE user_id=? ORDER BY id DESC LIMIT 1", (user_id,))
    session_id = cursor.fetchone()
    if session_id is None:
        return create_new_session(user_id)
    return int(session_id[0])
