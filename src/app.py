from flask import Flask
from flask import jsonify

from tiltometer import get_tilt

application = Flask(__name__)


@application.route('/')
def index():
    return "Hello, World!"


@application.route('/tilt-o-meter/<summoner_name>', methods=['GET'])
def tiltometer(summoner_name):
    return jsonify(get_tilt(summoner_name))
