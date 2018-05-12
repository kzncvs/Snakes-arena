import sqlite3
import json
from arena import STEPS_LIMIT

db_link = 'C:/Users/s/PycharmProjects/snakes_arena/snake.db'


def get_fight_count():
    db = sqlite3.connect(db_link)
    cursor = db.cursor()
    cursor.execute('SELECT Count(*) FROM fights')
    heh = cursor.fetchone()[0]
    db.close()
    return heh


def is_fight_waiting(fight_id):
    db = sqlite3.connect(db_link)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM fights WHERE [fight_id] = :count',
                   {'count': fight_id})
    heh = cursor.fetchone()
    db.close()
    return heh[2] is None


def is_last_fight_waiting():
    return is_fight_waiting(get_fight_count())


def append_snake(snake_id):
    db = sqlite3.connect(db_link)
    cursor = db.cursor()
    cursor.execute('UPDATE [fights] SET [snake2] = :snake WHERE fight_id = :count',
                   {'snake': snake_id, 'count': get_fight_count()})

    snake1_head = [6, 7]
    snake1_body = [[5, 7], [4, 7], [3, 7]]
    snake1_tail = [2, 7]

    snake2_head = [3, 2]
    snake2_body = [[4, 2], [5, 2], [6, 2]]
    snake2_tail = [7, 2]
    cursor.execute('UPDATE [fights] SET [snake1_head] = :snake1_head WHERE fight_id = :count',
                   {'snake1_head': json.dumps(snake1_head), 'count': get_fight_count()})
    cursor.execute('UPDATE [fights] SET [snake1_body] = :snake1_body WHERE fight_id = :count',
                   {'snake1_body': json.dumps(snake1_body), 'count': get_fight_count()})
    cursor.execute('UPDATE [fights] SET [snake1_tail] = :snake1_tail WHERE fight_id = :count',
                   {'snake1_tail': json.dumps(snake1_tail), 'count': get_fight_count()})
    cursor.execute('UPDATE [fights] SET [snake2_head] = :snake2_head WHERE fight_id = :count',
                   {'snake2_head': json.dumps(snake2_head), 'count': get_fight_count()})
    cursor.execute('UPDATE [fights] SET [snake2_body] = :snake2_body WHERE fight_id = :count',
                   {'snake2_body': json.dumps(snake2_body), 'count': get_fight_count()})
    cursor.execute('UPDATE [fights] SET [snake2_tail] = :snake2_tail WHERE fight_id = :count',
                   {'snake2_tail': json.dumps(snake2_tail), 'count': get_fight_count()})
    cursor.execute('UPDATE [fights] SET [snake2_bited] = 0 WHERE fight_id = :count',
                   {'count': get_fight_count()})
    cursor.execute('UPDATE [fights] SET [snake1_bited] = 0 WHERE fight_id = :count',
                   {'count': get_fight_count()})
    cursor.execute('UPDATE [fights] SET [steps_left] = :steps_left WHERE fight_id = :count',
                   {'steps_left': STEPS_LIMIT, 'count': get_fight_count()})

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


def get_fight_info(fight_id):
    db = sqlite3.connect(db_link)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM fights WHERE [fight_id] = :count',
                   {'count': fight_id})
    heh = cursor.fetchone()
    db.close()
    return heh
