from . import cursor, database
import datetime


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def check_subscribed(user_id):
    print("Проверяю подписку...")
    cursor.execute("SELECT register FROM User WHERE id=?", (user_id,))
    register = datetime.datetime.strptime(cursor.fetchone()[0], DATE_FORMAT)
    print("Дата регистрации:", register)
    if register <= datetime.datetime.now() + datetime.timedelta(days=2):
        print("Действует пробный период", register)
        return True
    print("Проверяем подписку", register)
    cursor.execute("SELECT subscribed FROM User WHERE id=?", (user_id,))
    subscribed = bool(cursor.fetchone()[0])
    return subscribed


def subscribe(user_id):
    cursor.execute("UPDATE User SET subscribed = 1 WHERE id=?;", (user_id,))
    database.commit()


def unsubscribe(user_id):
    cursor.execute("UPDATE User SET subscribed = 0 WHERE id=?;", (user_id,))
    database.commit()
