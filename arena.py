from flask import *
import db_tools
import uuid

STEPS_LIMIT = 30


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
        db_tools.change_fight_info(battle_id, snake1_head=snake1_head, snake1_body=snake1_body, snake1_tail=snake1_tail,
                                   snake2_head=snake2_head, snake2_body=snake2_body, snake2_tail=snake2_tail,
                                   is1bited=False, is2bited=False, steps_left=STEPS_LIMIT, snake2_id=snake_id,
                                   snake1_step=False, snake2_step=False, snake1_score=0, snake2_score=0, winner=0)
        return {'battle_id': battle_id, 'snake_id': snake_id}
    else:
        snake_id = uuid.uuid1().int % 10000000
        battle_id = db_tools.fight_init(snake_id)
        return {'battle_id': battle_id, 'snake_id': snake_id}


def battle_tick(snake_id, battle_id):
    if db_tools.is_fight_waiting(battle_id):
        return jsonify({}), 202
    if db_tools.is_snake_waiting(snake_id, battle_id):
        return jsonify({}), 202
    end = db_tools.is_battle_ended(snake_id, battle_id)
    if end:
        return jsonify(end), 200
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
        else:
            return jsonify({}), 400
        return jsonify(response), 200


def make_step(snake_id, battle_id, direction):
    if db_tools.is_steps_made(battle_id):
        return jsonify({}), 400
    else:
        battle_info = db_tools.get_fight_info(battle_id)
        if battle_info[1] == snake_id:
            db_tools.change_fight_info(battle_id, snake1_step=direction)
        elif battle_info[2] == snake_id:
            db_tools.change_fight_info(battle_id, snake2_step=direction)
        else:
            return jsonify({}), 400
        if db_tools.is_steps_made(battle_id):
            compute_step()
        return jsonify({}), 200


def compute_step():
    print("keeeeeeeek")
