import traceback

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from tiltometer import get_tilt
from tilt_exceptions import SummonerNotFound

application = Flask(__name__)


# redirect all non existing urls to index.html
@application.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@application.route('/', methods=['GET'])
def index():
    return render_template('index.html', request=request)


@application.route('/tilt-o-meter/<summoner_name>', methods=['GET'])
def tiltometer(summoner_name):
    # return jsonify(get_tilt(summoner_name))
    try:
        data = get_tilt(summoner_name)
        return render_template('tiltometer.html', data=data)
    except SummonerNotFound as e:
        return render_template('404.html',
                               request=request,
                               error='{0}'.format(e))
    except:
        application.logger.error(traceback.format_exc())
        return render_template('404.html', request=request)


@application.route('/api/<summoner_name>', methods=['GET'])
def api(summoner_name):
    return jsonify(get_tilt(summoner_name))
