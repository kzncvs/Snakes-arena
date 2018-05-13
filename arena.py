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
    end = db_tools.is_battle_ended(snake_id, battle_id)
    if end:
        return jsonify(end), 200
    else:
        battle_info = db_tools.get_fight_info(battle_id)
        if battle_info[1] == snake_id:
            db_tools.change_fight_info(battle_id, snake1_step=direction)
        elif battle_info[2] == snake_id:
            db_tools.change_fight_info(battle_id, snake2_step=direction)
        else:
            return jsonify({}), 400
        if db_tools.is_steps_made(battle_id):
            compute_step(battle_id)
        return jsonify({}), 200


def compute_step(battle_id):
    battle_info = db_tools.get_fight_info(battle_id)
    current_snakes = {
        'snake1': {
            'head': json.loads(battle_info[4]),
            'body': json.loads(battle_info[5]),
            'tail': json.loads(battle_info[6]),
            'is_bited': bool(battle_info[7]),
            'step': battle_info[12]
        },
        'snake2': {
            'head': json.loads(battle_info[8]),
            'body': json.loads(battle_info[9]),
            'tail': json.loads(battle_info[10]),
            'is_bited': bool(battle_info[11]),
            'step': battle_info[13]
        }
    }

    new_head1 = []
    new_body1 = []
    new_tail1 = []
    if current_snakes['snake1']['step'] == 'pass':
        new_head1 = current_snakes['snake1']['head']
        new_body1 = current_snakes['snake1']['body']
        new_tail1 = current_snakes['snake1']['tail']
    else:
        if current_snakes['snake1']['step'] == 'up':
            new_head1 = [current_snakes['snake1']['head'][0], current_snakes['snake1']['head'][1] + 1]
        elif current_snakes['snake1']['step'] == 'down':
            new_head1 = [current_snakes['snake1']['head'][0], current_snakes['snake1']['head'][1] - 1]
        elif current_snakes['snake1']['step'] == 'right':
            new_head1 = [current_snakes['snake1']['head'][0] + 1, current_snakes['snake1']['head'][1]]
        elif current_snakes['snake1']['step'] == 'left':
            new_head1 = [current_snakes['snake1']['head'][0] - 1, current_snakes['snake1']['head'][1]]

        new_body1 = [current_snakes['snake1']['head']]
        new_body1.extend(current_snakes['snake1']['body'])
        new_tail1 = new_body1.pop()

    new_head2 = []
    new_body2 = []
    new_tail2 = []
    if current_snakes['snake2']['step'] == 'pass':
        new_head2 = current_snakes['snake2']['head']
        new_body2 = current_snakes['snake2']['body']
        new_tail2 = current_snakes['snake2']['tail']
    else:
        if current_snakes['snake2']['step'] == 'up':
            new_head2 = [current_snakes['snake2']['head'][0], current_snakes['snake2']['head'][1] + 1]
        elif current_snakes['snake2']['step'] == 'down':
            new_head2 = [current_snakes['snake2']['head'][0], current_snakes['snake2']['head'][1] - 1]
        elif current_snakes['snake2']['step'] == 'right':
            new_head2 = [current_snakes['snake2']['head'][0] + 1, current_snakes['snake2']['head'][1]]
        elif current_snakes['snake2']['step'] == 'left':
            new_head2 = [current_snakes['snake2']['head'][0] - 1, current_snakes['snake2']['head'][1]]

        new_body2 = [current_snakes['snake2']['head']]
        new_body2.extend(current_snakes['snake2']['body'])
        new_tail2 = new_body2.pop()

    is_snake1_died = new_head1[0] > 9 or new_head1[0] < 0 or new_head1[1] > 9 or new_head1[
        1] < 0 or new_head1 in new_body1 or new_head1 in new_body2 or new_head1 == new_head2
    is_snake2_died = new_head2[0] > 9 or new_head2[0] < 0 or new_head2[1] > 9 or new_head2[
        1] < 0 or new_head2 in new_body1 or new_head2 in new_body2 or new_head1 == new_head2

    if is_snake1_died and is_snake2_died:
        db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                   snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                   snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                   snake2_step=False, winner=-1)
        return
    elif is_snake1_died:
        db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                   snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                   snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                   snake2_step=False, winner=2)
        return
    elif is_snake2_died:
        db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                   snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                   snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                   snake2_step=False, winner=1)
        return

