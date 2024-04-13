from . import database, cursor
from datetime import datetime


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def check_payment(user_id):
    cursor.execute("SELECT paid_by FROM User WHERE id=?", (user_id,))
    paid_by = datetime.strptime(cursor.fetchone()[0], DATE_FORMAT)
    if paid_by >= datetime.now():
        return True
    return False
