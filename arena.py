STEPS_LIMIT = 30

from flask import *
import db_tools
import uuid


def battle_init():
    if db_tools.is_last_fight_waiting():
        battle_id = db_tools.get_fight_count()
        snake_id = uuid.uuid1().int % 10000000
        snake1_head = [6, 7]
        snake1_body = [[5, 7], [4, 7], [3, 7]]
        snake1_tail = [2, 7]
        snake2_head = [3, 2]
        snake2_body = [[4, 2], [5, 2], [6, 2]]
        snake2_tail = [7, 2]
        db_tools.change_fight_info(snake1_head=snake1_head, snake1_body=snake1_body, snake1_tail=snake1_tail,
                                   snake2_head=snake2_head, snake2_body=snake2_body, snake2_tail=snake2_tail,
                                   is1bited=False, is2bited=False, steps_left=STEPS_LIMIT, snake2_id=snake_id)
        return {'battle_id': battle_id, 'snake_id': snake_id}
    else:
        snake_id = uuid.uuid1().int % 10000000
        battle_id = db_tools.fight_init(snake_id)
        return {'battle_id': battle_id, 'snake_id': snake_id}


def battle_tick(snake_id, battle_id):
    if db_tools.is_fight_waiting(battle_id) is True:
        return jsonify({}), 202
    else:
        battle_info = db_tools.get_fight_info(battle_id)
        snake1 = {
            'head': json.loads(battle_info[4]),
            'body': json.loads(battle_info[5]),
            'tail': json.loads(battle_info[6]),
            'is_bited': bool(battle_info[7])
        }
        snake2 = {
            'head': json.loads(battle_info[8]),
            'body': json.loads(battle_info[9]),
            'tail': json.loads(battle_info[10]),
            'is_bited': bool(battle_info[11])
        }
        response = {}
        if battle_info[1] == snake_id:
            response = {
                'snakes': {'ally': snake1, 'enemy': snake2},
                'battle': {'steps_left': battle_info[3], 'battle_id': battle_id, 'snake_id': snake_id}
            }
        elif battle_info[2] == snake_id:
            response = {
                'snakes': {'ally': snake2, 'enemy': snake1},
                'battle': {'steps_left': battle_info[3], 'battle_id': battle_id, 'snake_id': snake_id}
            }
        return jsonify(response), 200
