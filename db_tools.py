import sqlite3
import json

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


def change_fight_info(snake1_head=None, snake1_body=None, snake1_tail=None, snake2_head=None, snake2_body=None,
                      snake2_tail=None, steps_left=None, is1bited=None, is2bited=None, snake2_id=None):
    db = sqlite3.connect(db_link)
    cursor = db.cursor()
    if snake1_head is not None:
        cursor.execute('UPDATE [fights] SET [snake1_head] = :snake1_head WHERE fight_id = :count',
                       {'snake1_head': json.dumps(snake1_head), 'count': get_fight_count()})
    if snake1_body is not None:
        cursor.execute('UPDATE [fights] SET [snake1_body] = :snake1_body WHERE fight_id = :count',
                       {'snake1_body': json.dumps(snake1_body), 'count': get_fight_count()})
    if snake1_tail is not None:
        cursor.execute('UPDATE [fights] SET [snake1_tail] = :snake1_tail WHERE fight_id = :count',
                       {'snake1_tail': json.dumps(snake1_tail), 'count': get_fight_count()})
    if snake2_head is not None:
        cursor.execute('UPDATE [fights] SET [snake2_head] = :snake2_head WHERE fight_id = :count',
                       {'snake2_head': json.dumps(snake2_head), 'count': get_fight_count()})
    if snake2_body is not None:
        cursor.execute('UPDATE [fights] SET [snake2_body] = :snake2_body WHERE fight_id = :count',
                       {'snake2_body': json.dumps(snake2_body), 'count': get_fight_count()})
    if snake2_tail is not None:
        cursor.execute('UPDATE [fights] SET [snake2_tail] = :snake2_tail WHERE fight_id = :count',
                       {'snake2_tail': json.dumps(snake2_tail), 'count': get_fight_count()})
    if is2bited is not None:
        cursor.execute('UPDATE [fights] SET [snake2_bited] = :isbited WHERE fight_id = :count',
                       {'count': get_fight_count(), 'isbited': int(is2bited)})
    if is1bited is not None:
        cursor.execute('UPDATE [fights] SET [snake1_bited] = :isbited WHERE fight_id = :count',
                       {'count': get_fight_count(), 'isbited': int(is1bited)})
    if steps_left is not None:
        cursor.execute('UPDATE [fights] SET [steps_left] = :steps_left WHERE fight_id = :count',
                       {'steps_left': steps_left, 'count': get_fight_count()})
    if snake2_id is not None:
        cursor.execute('UPDATE [fights] SET [snake2] = :snake WHERE fight_id = :count',
                       {'snake': snake2_id, 'count': get_fight_count()})
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
