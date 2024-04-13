from . import database, cursor
from loader import gpt


def check_payment(user_id):
    cursor.execute("SELECT paid_by FROM User WHERE user_id=?", (user_id,))
    paid_by = cursor.fetchone()[0]
    print("Оплачено до:", paid_by)
    return True
