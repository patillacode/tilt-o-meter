from riotwatcher import RiotWatcher
from riotwatcher import EUROPE_WEST

from config import API_KEY

euw = RiotWatcher(API_KEY, default_region=EUROPE_WEST)
# check if we have API calls remaining
print(euw.can_make_request())

player = euw.get_summoner(name='Yocta', region=EUROPE_WEST)
print(player)

#ranked_stats = euw.get_ranked_stats(player['id'])
#print(ranked_stats)

games_won = 0
recent_games = euw.get_recent_games(player['id'])
for game in recent_games['games']:
  if game['stats']['win']:
    games_won += 1
  #for k, v in game.iteritems():
  #  print k, v
  #  print "-" * 30
  #print "#" * 30

print "{0}/10 games won".format(games_won)
