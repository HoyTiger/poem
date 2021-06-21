from flask import Blueprint, jsonify
from model import Poem
poem = Blueprint('poem', __name__)

@poem.route('/list')
def list_poem():
    data = {}
    try:
        poems = Poem.query.all()
        print(poems)
        output = []
        for poem in poems:
            output.append(poem.to_json())
        data['data'] = output
        data['code'] = 0
    except Exception as e:
        print(e)
        data['code'] = 1
    return jsonify(data)



