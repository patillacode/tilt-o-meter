import traceback

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from tiltometer import get_tilt

application = Flask(__name__)


@application.route('/hello/')
@application.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@application.route('/', methods=['GET'])
def index(summoner_name):
    return render_template('index.html')


@application.route('/tilt-o-meter/<summoner_name>', methods=['GET'])
def tiltometer(summoner_name):
    # return jsonify(get_tilt(summoner_name))
    try:
        data = get_tilt(summoner_name)
        return render_template('tiltometer.html', data=data)
    except:
        application.logger.error(traceback.format_exc())
        return render_template('404.html', request=request)


@application.route('/api/<summoner_name>', methods=['GET'])
def api(summoner_name):
    return jsonify(get_tilt(summoner_name))
