from flask import *
import arena

app = Flask(__name__)


@app.route('/snake', methods=['POST'])
def get_request():
    print(request.json)

    # IF NO JSON
    if not request.json:
        abort(400)

    # INIT REQUEST
    elif 'answer' in request.json:
        if request.json['answer'] == '42':
            return jsonify(arena.battle_init()), 201

    # STEP REQUEST
    elif 'step' in request.json and 'snake_id' in request.json and 'battle_id' in request.json:
        return arena.make_step(request.json['snake_id'], request.json['battle_id'], request.json['step'])

    # ЕСТЬ ЧЁ REQUEST
    elif 'snake_id' in request.json and 'battle_id' in request.json:
        return arena.battle_tick(request.json['snake_id'], request.json['battle_id'])

    # IF INVALID JSON
    else:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True)
