import sqlite3
from cpu import get_cpu_usage


def statistic():
    return f"Статистика бота:\n\n{how_many_people()}\n\n{get_cpu_usage()}"


def how_many_people():
    con = sqlite3.connect('chatgpt.db')
    cursor = con.cursor()
    return f"Всего людей: {len(cursor.execute('SELECT id FROM chatgpt').fetchall())}"
