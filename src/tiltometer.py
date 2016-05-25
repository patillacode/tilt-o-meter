# import argparse
import logging
import random
import sys
import traceback

import config

from riotwatcher import EUROPE_WEST
from riotwatcher import RiotWatcher

from keys import API_KEY

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

global champions_dict


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
        kills = game['stats'].get('championsKilled', 0)
        deaths = game['stats'].get('numDeaths', 0)
        assists = game['stats'].get('assists', 0)

        champion_name = get_champion_name_by_id(game['championId'],
                                                champions_dict)
        champion_img = "{0}{1}.png".format(config.CHAMPION_ICON_URL,
                                           champion_name)
        position = game['stats'].get('playerPosition', 'N/A')
        pentakill = True if game['stats'].get('largestMultiKill', 0) == 5 \
            else False

        time = game['stats']['timePlayed']
        game_mode = game['gameMode']
        win = False

        if game['stats']['win']:
            win = True

        g = {'kills': kills,
             'deaths': deaths,
             'assists': assists,
             'champion_name': champion_name,
             'champion_img': champion_img,
             'position': position,
             'pentakill': pentakill,
             'time': time,
             'game_mode': game_mode,
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
                                 random_champion_name)


def get_random_display():
    return random.choice(config.TILT_DISPLAYS)


def get_tilt(summoner_name):
    try:
        euw = RiotWatcher(API_KEY, default_region=EUROPE_WEST)
        champions_dict = get_champions_data(euw)
        # check if we have API calls remaining
        if euw.can_make_request():
            logger.debug('Requests to API available')
        else:
            logger.error('Too many requests. Please wait.')
            sys.exit(2)

        player = euw.get_summoner(name=summoner_name, region=EUROPE_WEST)
        recent_games = euw.get_recent_games(player['id'])['games']

        response = {"status": 200,
                    "wins": get_wins_number(recent_games),
                    "metadata": {
                        "background": get_random_background_url(
                            champions_dict),
                        "display": get_random_display()},
                    "stats": get_stats(recent_games, champions_dict)}
        return response
    except:
        print traceback.format_exc()
        return {'error': 'an error ocurred, please try again.'}


# if __name__ == '__main__':

#     parser = argparse.ArgumentParser(
#         description='Measure a player\'s strike in LOL - last 10 games')
#     parser.add_argument('-n',
#                         '--name',
#                         metavar='name',
#                         type=str,
#                         required=True,
#                         help='Player\'s name')

#     args = parser.parse_args()
#     name = args.name

#     print get_tilt(name)
