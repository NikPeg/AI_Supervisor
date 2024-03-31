import datetime
from loader import database,cursor

def get_user_sessia_id(user_id):
    cursor.execute("SELECT sessia_id FROM Sessies WHERE user_id=?",(user_id,))
    sessia_id = cursor.fetchone()
    if sessia_id is None:
        return int(0)
    return int(sessia_id[0])

def create_new_sessia(user_id):
    sessia_id = get_user_sessia_id(user_id)
    sessia_id += int(1)
    date = datetime.datetime.now()
    cursor.execute("INSERT INTO Sessies VALUES(?,?,?)",(user_id,sessia_id,date,))
    database.commit()