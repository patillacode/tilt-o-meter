import logging
import argparse
import sys

from riotwatcher import RiotWatcher
from riotwatcher import EUROPE_WEST

from config import API_KEY

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Measure a player\'s strike in LOL - last 10 games')
    parser.add_argument('-n',
                        '--name',
                        metavar='name',
                        type=str,
                        required=True,
                        help='Player\'s name')

    args = parser.parse_args()
    name = args.name

    euw = RiotWatcher(API_KEY, default_region=EUROPE_WEST)

    # check if we have API calls remaining
    if euw.can_make_request():
        logger.debug('Requests to API available')
    else:
        logger.error('Too many requests. Please wait.')
        sys.exit(2)

    champions_list = euw.static_get_champion_list()['data']
    champions_dict = {}
    for data in champions_list.values():
        champions_dict[data['id']] = data['name']

    games_won = 0
    kills = 0
    deaths = 0
    assists = 0

    player = euw.get_summoner(name=name, region=EUROPE_WEST)
    recent_games = euw.get_recent_games(player['id'])

    print ' ', '-' * 39
    for game in recent_games['games']:
        # for k, v in game.iteritems():
        #     print k, v
        #     print "-" * 30
        # print "#" * 30
        kills = game['stats'].get('championsKilled', 0)
        deaths = game['stats'].get('numDeaths', 0)
        assists = game['stats'].get('assists', 0)

        game_result = 'LOST'
        if game['stats']['win']:
            games_won += 1
            game_result = 'WON'

        champ_colum = '  {0} '.format(
            champions_dict[game['championId']]).ljust(18)
        kda_column = '   {0}/{1}/{2} '.format(kills, deaths, assists).ljust(12)
        result_column = '  {0} '.format(game_result).ljust(8)
        print ' |{0}|{1}|{2}|'.format(champ_colum, kda_column, result_column)
        print ' ', '-' * 39

    print "{0}: {1}/10 games won".format(name, games_won)

    # ranked_stats = euw.get_ranked_stats(player['id'])
    # print(ranked_stats)
