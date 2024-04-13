from . import database, cursor
from datetime import datetime


def check_payment(user_id):
    cursor.execute("SELECT paid_by FROM User WHERE id=?", (user_id,))
    paid_by = cursor.fetchone()[0]
    print("Оплачено до:", paid_by)
    if paid_by >= datetime.now():
        return True
    return False
