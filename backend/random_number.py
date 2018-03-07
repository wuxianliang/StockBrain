from flask import jsonify
from random import *
def get_random_number():
    response = {
        'randomNumber': randint(1, 2)
    }
    return jsonify(response)
