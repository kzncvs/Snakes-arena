import sqlite3

db_link = 'C:/Users/s/PycharmProjects/snakes_arena/snake.db'


def get_fight_count():
    db = sqlite3.connect(db_link)
    cursor = db.cursor()
    cursor.execute('SELECT Count(*) FROM fights')
    heh = cursor.fetchone()[0]
    db.close()
    return heh


def is_last_fight_waiting():
    db = sqlite3.connect(db_link)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM fights WHERE [fight_id] = :count',
                   {'count': get_fight_count()})
    heh = cursor.fetchone()
    db.close()
    return heh[2] is None


def append_snake(snake_id):
    db = sqlite3.connect(db_link)
    cursor = db.cursor()
    cursor.execute('UPDATE [fights] SET [snake2] = :snake WHERE fight_id = :count',
                   {'snake': snake_id, 'count': get_fight_count()})
    db.commit()
    db.close()


def fight_init(snake_id):
    db = sqlite3.connect(db_link)
    cursor = db.cursor()
    cursor.execute('INSERT INTO [fights] ([fight_id], [snake1]) VALUES (:fight, :snake)',
                   {'fight': get_fight_count() + 1, 'snake': snake_id})
    db.commit()
    db.close()
    return get_fight_count()