import random
import sys
import traceback

import config

from flask import current_app

from riotwatcher import EUROPE_WEST
from riotwatcher import RiotWatcher

from keys import API_KEY


def get_champions_data(watcher):
    champions_list = watcher.static_get_champion_list()['data']
    champions_dict = {}
    for data in champions_list.values():
        champions_dict[data['id']] = data['name']

    return champions_dict


def get_champion_name_by_id(champion_id, champions_dict):
    return champions_dict[champion_id]


def get_stats(games, champions_dict):
    stats = []

    for game in games:
        print game
        kills = game['stats'].get('championsKilled', 0)
        deaths = game['stats'].get('numDeaths', 0)
        assists = game['stats'].get('assists', 0)

        champion_name = get_champion_name_by_id(game['championId'],
                                                champions_dict)
        champion_img = "{0}{1}.png".format(config.CHAMPION_ICON_URL,
                                           champion_name.replace('\'', ''))
        position = game['stats'].get('playerPosition', 0)
        pentakill = True if game['stats'].get('largestMultiKill', 0) == 5 \
            else False

        time = game['stats']['timePlayed']
        game_type = game['subType']
        win = False

        if game['stats']['win']:
            win = True

        g = {'kills': kills,
             'deaths': deaths,
             'assists': assists,
             'champion_name': champion_name,
             'champion_img': champion_img,
             'position': config.PLAYER_POSITION[position],
             'pentakill': pentakill,
             'time': '{0}:{1}'.format(time / 60, str(time % 60).zfill(2)),
             'game_type': game_type,
             'win': win}

        stats.append(g)

    return stats


def get_wins_number(games):
    wins_number = 0
    for game in games:
        if game['stats']['win']:
            wins_number += 1
    return wins_number


def get_random_background_url(champions_dict):
    random_champion_name = random.sample(champions_dict.values(), 1)[0]
    return "{0}{1}_0.jpg".format(config.CHAMPION_SPLASH_URL,
                                 random_champion_name.replace('\'', ''))


def get_random_display():
    return random.choice(config.TILT_DISPLAYS)


def get_kda(kills, deaths, assists):
    return (kills + deaths) / max(1, deaths)


def get_tilt_level(games):
    # this is a subjective algorithm to measure someone's tilt
    # completely arbitrary - over a 100 point scale
    tilt_points = 0
    multiplier = 10

    for game in games:
        # 0.5 tilt points for every game lost
        # bigger multiplier the more recent the game was
        if not game['stats']['win']:
            tilt_points += 0.8 * multiplier

            # if you lost a game under 25 minutes probably means you forfited
            # or you were crushed
            # multiplier for the more recent was
            if game['stats']['timePlayed'] < 1500:
                tilt_points += 1 * multiplier

        # if you lost X games in a row you gain 10 tilt points per game
        # bigger multiplier the more recent the cold strike was

        # if your KDA is low... tilt points for you!
        kda = get_kda(game['stats'].get('championsKilled', 0),
                      game['stats'].get('numDeaths', 0),
                      game['stats'].get('assists', 0))
        if kda < 1:
            tilt_points += 1.5 * multiplier
        elif kda < 2:
            tilt_points += 1 * multiplier
        elif kda < 3:
            tilt_points += 0.5 * multiplier
        # if your kda is over 3 you did fairly well adn you are happy
        # let's get some tilt point off of you ^^
        else:
            tilt_points -= 1 * multiplier

        multiplier -= 1

    return tilt_points


def get_tilt(summoner_name):
    try:
        euw = RiotWatcher(API_KEY, default_region=EUROPE_WEST)
        champions_dict = get_champions_data(euw)
        # check if we have API calls remaining
        if euw.can_make_request():
            current_app.logger.debug('Requests to API available')
        else:
            current_app.logger.error('Too many requests. '
                                     'Please try again later.')
            sys.exit(2)

        player = euw.get_summoner(name=summoner_name, region=EUROPE_WEST)
        recent_games = euw.get_recent_games(player['id'])['games']

        response = {"status": 200,
                    "wins": get_wins_number(recent_games),
                    "metadata": {
                        "background": get_random_background_url(
                            champions_dict),
                        "display": get_random_display()},
                    "stats": get_stats(recent_games, champions_dict),
                    "summoner_name": summoner_name,
                    "tilt_level": get_tilt_level(recent_games)}
        return response
    except:
        current_app.logger.error(traceback.format_exc())
        raise
        # return {'error': 'an error ocurred, please try again.'}
