from flask import (
    Blueprint,
    current_app,
    # flash,
    # redirect,
    render_template,
    request,
    # url_for,
)
from riotwatcher import LolWatcher
from .secrets import RIOT_API_KEY
from .utils import Tiltometer, get_champions_data

bp = Blueprint('tiltometer', __name__)
lol_watcher = LolWatcher(RIOT_API_KEY)
champions_data = get_champions_data(lol_watcher, 'euw1')


@bp.route('/')
def index():
    return render_template(
        'index.html', request=request, host=current_app.config.get('DOMAIN')
    )


@bp.route('/tilt-o-meter/<region>/<summoner_name>', methods=('GET',))
def tiltometer(region, summoner_name):
    try:
        tiltometer = Tiltometer(lol_watcher, region, summoner_name, champions_data)
        data = tiltometer.get_tilt()
        return render_template('tiltometer.html', data=data)

    except Exception as err:
        current_app.logger.error(err)
        return render_template('404.html', request=request)
