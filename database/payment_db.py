from . import cursor
import datetime


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def check_subscribed(user_id):
    cursor.execute("SELECT register FROM User WHERE id=?", (user_id,))
    register = datetime.datetime.strptime(cursor.fetchone()[0], DATE_FORMAT)
    if register <= datetime.datetime.now() + datetime.timedelta(days=2):
        return True
    cursor.execute("SELECT subscribed FROM User WHERE id=?", (user_id,))
    subscribed = bool(cursor.fetchone()[0])
    return subscribed
