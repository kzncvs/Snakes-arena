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
        snake1_last_tail = [1, 7]
        snake1_last_last = [0, 7]
        snake2_head = [3, 2]
        snake2_body = [[4, 2], [5, 2], [6, 2]]
        snake2_tail = [7, 2]
        snake2_last_tail = [8, 2]
        snake2_last_last = [9, 2]

        db_tools.change_fight_info(battle_id, snake1_head=snake1_head, snake1_body=snake1_body, snake1_tail=snake1_tail,
                                   snake2_head=snake2_head, snake2_body=snake2_body, snake2_tail=snake2_tail,
                                   is1bited=False, is2bited=False, steps_left=STEPS_LIMIT, snake2_id=snake_id,
                                   snake1_step=False, snake2_step=False, snake1_score=0, snake2_score=0, winner=0,
                                   last_tail1=snake1_last_tail, last_tail2=snake2_last_tail,
                                   snake1_last_last=snake1_last_last, snake2_last_last=snake2_last_last)
        arena_print(battle_id)
        return {'battle_id': battle_id, 'snake_id': snake_id}
    else:
        snake_id = uuid.uuid1().int % 10000000
        battle_id = db_tools.fight_init(snake_id)
        return {'battle_id': battle_id, 'snake_id': snake_id}


def battle_tick(snake_id, battle_id):
    if db_tools.is_fight_waiting(battle_id) or db_tools.is_snake_waiting(snake_id, battle_id):
        return jsonify({}), 202
    end = db_tools.is_battle_ended(snake_id, battle_id)
    if end:
        return jsonify(end), 200

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
    if db_tools.is_steps_made(battle_id) or db_tools.is_snake_passing(snake_id, battle_id):
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
            'step': battle_info[12],
            'last_tail': json.loads(battle_info[17]),
            'last_last_tail': json.loads(battle_info[29])
        },
        'snake2': {
            'head': json.loads(battle_info[8]),
            'body': json.loads(battle_info[9]),
            'tail': json.loads(battle_info[10]),
            'is_bited': bool(battle_info[11]),
            'step': battle_info[13],
            'last_tail': json.loads(battle_info[18]),
            'last_last_tail': json.loads(battle_info[20])
        }
    }

    if current_snakes['snake1']['is_bited']:
        db_tools.change_fight_info(battle_id, is1bited=False)
    if current_snakes['snake2']['is_bited']:
        db_tools.change_fight_info(battle_id, is2bited=False)

    new_head1 = []
    new_body1 = []
    new_tail1 = []
    new_last1 = []
    if current_snakes['snake1']['step'] == 'pass':
        new_head1 = current_snakes['snake1']['head']
        new_body1 = current_snakes['snake1']['body']
        new_body1.append(current_snakes['snake1']['tail'])
        new_tail1 = current_snakes['snake1']['last_tail']
        new_last1 = current_snakes['snake1']['last_last_tail']

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
        new_last1 = current_snakes['snake1']['last_last_tail']
        if current_snakes['snake1']['is_bited']:
            new_tail1 = new_body1.pop()

    new_head2 = []
    new_body2 = []
    new_tail2 = []
    new_last2 = []
    if current_snakes['snake2']['step'] == 'pass':
        new_head2 = current_snakes['snake2']['head']
        new_body2 = current_snakes['snake2']['body']
        new_body2.append(current_snakes['snake2']['tail'])
        new_tail2 = current_snakes['snake2']['last_tail']
        new_last2 = current_snakes['snake2']['last_last_tail']

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
        new_last2 = current_snakes['snake2']['last_last_tail']
        if current_snakes['snake2']['is_bited']:
            new_tail2 = new_body2.pop()

    is_snake1_died = new_head1[0] > 9 or new_head1[0] < 0 or new_head1[1] > 9 or new_head1[
        1] < 0 or new_head1 in new_body1 or new_head1 in new_body2 or new_head1 == new_head2 or new_head1 == new_tail1
    is_snake2_died = new_head2[0] > 9 or new_head2[0] < 0 or new_head2[1] > 9 or new_head2[
        1] < 0 or new_head2 in new_body1 or new_head2 in new_body2 or new_head1 == new_head2 or new_head2 == new_tail2

    if is_snake1_died and is_snake2_died:
        db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                   snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                   snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                   snake2_step=False, winner=-1)
        arena_print(battle_id)
        return
    elif is_snake1_died:
        db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                   snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                   snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                   snake2_step=False, winner=2)
        arena_print(battle_id)
        return
    elif is_snake2_died:
        db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                   snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                   snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                   snake2_step=False, winner=1)
        arena_print(battle_id)
        return

    if new_head1 == new_tail2:
        if len(new_body2) == 0:
            db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                       snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                       snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                       snake2_step=False, winner=1, snake1_score=battle_info[14] + 1,
                                       last_tail1=current_snakes['snake1']['tail'],
                                       last_tail2=current_snakes['snake2']['tail'])
            arena_print(battle_id)
            return
        else:
            db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                       snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                       snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step='pass',
                                       snake2_step=False, is1bited=False, is2bited=True,
                                       snake1_score=battle_info[14] + 1, last_tail1=current_snakes['snake1']['tail'],
                                       last_tail2=current_snakes['snake2']['tail'])
            arena_print(battle_id)
            return

    if new_head2 == new_tail1:
        if len(new_body2) == 0:
            db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                       snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                       snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                       snake2_step=False, winner=2, snake1_score=battle_info[15] + 1,
                                       last_tail1=current_snakes['snake1']['tail'],
                                       last_tail2=current_snakes['snake2']['tail'])
            arena_print(battle_id)
            return
        else:
            db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                       snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                       snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                       snake2_step='pass', is2bited=False, is1bited=True,
                                       snake2_score=battle_info[15] + 1, last_tail1=current_snakes['snake1']['tail'],
                                       last_tail2=current_snakes['snake2']['tail'])
            arena_print(battle_id)
            return

    if battle_info[3] == 1:
        if battle_info[14] > battle_info[15]:
            db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                       snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                       snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                       snake2_step=False, winner=1)
        elif battle_info[14] < battle_info[15]:
            db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                       snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                       snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                       snake2_step=False, winner=2)
        else:
            db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                                       snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                                       snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                                       snake2_step=False, winner=-1)

    db_tools.change_fight_info(fight_id=battle_id, snake1_head=new_head1, snake1_body=new_body1,
                               snake1_tail=new_tail1, snake2_head=new_head2, snake2_body=new_body2,
                               snake2_tail=new_tail2, steps_left=battle_info[3] - 1, snake1_step=False,
                               snake2_step=False, last_tail1=new_last1,
                               snake1_last_last=current_snakes['snake1']['last_tail'],
                               last_tail2=new_last2, snake2_last_last=current_snakes['snake2']['last_tail'])
    arena_print(battle_id)
    return


def arena_print(battle_id):
    battle_info = db_tools.get_fight_info(battle_id)
    snakes = {
        'snake1': {
            'head': json.loads(battle_info[4]),
            'body': json.loads(battle_info[5]),
            'tail': json.loads(battle_info[6]),
        },
        'snake2': {
            'head': json.loads(battle_info[8]),
            'body': json.loads(battle_info[9]),
            'tail': json.loads(battle_info[10]),
        }
    }
    print('..........')
    print('battle ' + str(battle_id) + ' // step ' + str(battle_info[3]))
    print('snake1 ' + str(battle_info[14]) + ' // snake2 ' + str(battle_info[15]))
    string_layout = ".........."
    strings = [string_layout for _ in range(10)]
    try:
        strings[snakes['snake1']['head'][1]] = strings[snakes['snake1']['head'][1]][
                                               :9 - snakes['snake1']['head'][0]] + '1' + strings[
                                                                                             snakes['snake1']['head'][
                                                                                                 1]][
                                                                                         9 - snakes['snake1']['head'][
                                                                                             0] + 1:]
    except:
        pass
    try:
        strings[snakes['snake2']['head'][1]] = strings[snakes['snake2']['head'][1]][
                                               :9 - snakes['snake2']['head'][0]] + '2' + strings[
                                                                                             snakes['snake2']['head'][
                                                                                                 1]][
                                                                                         9 - snakes['snake2']['head'][
                                                                                             0] + 1:]
    except:
        pass
    for segment in snakes['snake1']['body']:
        strings[segment[1]] = strings[segment[1]][:9 - segment[0]] + '+' + strings[segment[1]][9 - segment[0] + 1:]
    for segment in snakes['snake2']['body']:
        strings[segment[1]] = strings[segment[1]][:9 - segment[0]] + '-' + strings[segment[1]][9 - segment[0] + 1:]
    strings[snakes['snake1']['tail'][1]] = strings[snakes['snake1']['tail'][1]][
                                           :9 - snakes['snake1']['tail'][0]] + '!' + strings[
                                                                                         snakes['snake1']['tail'][1]][
                                                                                     9 - snakes['snake1']['tail'][
                                                                                         0] + 1:]
    strings[snakes['snake2']['tail'][1]] = strings[snakes['snake2']['tail'][1]][
                                           :9 - snakes['snake2']['tail'][0]] + '@' + strings[
                                                                                         snakes['snake2']['tail'][1]][
                                                                                     9 - snakes['snake2']['tail'][
                                                                                         0] + 1:]
    print('y 0123456789')
    for i in reversed(range(10)):
        print(i, strings[i][::-1], i)
    print('  0123456789 >x')
