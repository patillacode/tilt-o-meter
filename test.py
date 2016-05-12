from riotwatcher import RiotWatcher
from riotwatcher import EUROPE_WEST

from config import API_KEY

euw = RiotWatcher(API_KEY, default_region=EUROPE_WEST)
# check if we have API calls remaining
print(euw.can_make_request())

me = euw.get_summoner(name='dvitto', region=EUROPE_WEST)
print(me)
