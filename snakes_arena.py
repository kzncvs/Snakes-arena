from flask import *
import arena

app = Flask(__name__)


@app.route('/snake', methods=['POST'])
def get_request():
    print(request.json)
    if 'answer' in request.json:
        if request.json['answer'] == '42':
            return jsonify(arena.battle_init()), 201




if __name__ == '__main__':
    app.run(debug=True)
