import sqlite3


class Database:
    def __init__(self, user):
        self.user = user
        search_user(user)

    def get_translate(self):
        get_connect = sqlite3.connect('chatgpt.db')
        get_cursor = get_connect.cursor()
        return get_cursor.execute(f'SELECT translate FROM chatgpt WHERE id = {self.user}').fetchone()[0]

    def get_temperature(self):
        get_connect = sqlite3.connect('chatgpt.db')
        get_cursor = get_connect.cursor()
        return get_cursor.execute(f'SELECT temperature FROM chatgpt WHERE id = {self.user}').fetchone()[0]

    def get_switch(self):
        get_connect = sqlite3.connect('chatgpt.db')
        get_cursor = get_connect.cursor()
        return get_cursor.execute(f'SELECT switch FROM chatgpt WHERE id = {self.user}').fetchone()[0]


def save_value(user, **kwargs):
    save_connect = sqlite3.connect('chatgpt.db')
    save_cursor = save_connect.cursor()
    if 'translate' in kwargs:
        save_cursor.execute("UPDATE chatgpt SET translate = ? WHERE id = ?", (kwargs['translate'], user,))
    if 'temperature' in kwargs:
        save_cursor.execute("UPDATE chatgpt SET temperature = ? WHERE id = ?", (kwargs['temperature'], user,))
    if 'switch' in kwargs:
        save_cursor.execute("UPDATE chatgpt SET switch = ? WHERE id = ?", (kwargs['switch'], user,))
    save_connect.commit()


def search_table():
    search_connect = sqlite3.connect('chatgpt.db')
    search_cursor = search_connect.cursor()
    if len(search_cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' and name='chatgpt'").fetchall()) == 0:
        search_cursor.execute(
            "CREATE TABLE chatgpt(id INT, translate BOOLEAN, temperature INT, switch BOOLEAN)")


def search_user(user):
    search_connect = sqlite3.connect('chatgpt.db')
    search_cursor = search_connect.cursor()

    if search_cursor.execute("SELECT id FROM chatgpt WHERE id = ?", (user,)).fetchone() is None:
        search_cursor.execute("INSERT INTO chatgpt VALUES (?, ?, ?, ?)", (user, False, 0.5, False))

    search_connect.commit()