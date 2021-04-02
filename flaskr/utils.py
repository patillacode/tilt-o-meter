import datetime

from riotwatcher import ApiError
from flask import current_app


def get_champions_data(watcher, region):
    versions = watcher.data_dragon.versions_for_region(region)
    champions_version = versions['n']['champion']

    champions = watcher.data_dragon.champions(champions_version)['data']
    # {
    #     'Aatrox': {
    #         'version': '11.7.1',
    #         'id': 'Aatrox',
    #         'key': '266',
    #         'name': 'Aatrox',
    #         'title': 'the Darkin Blade',
    #         'blurb': 'Once honored defenders of Shurima against the Void, Aatrox and his brethren would eventually become an even greater threat to Runeterra, and were defeated only by cunning mortal sorcery. But after centuries of imprisonment, Aatrox was the first to find...',
    #         'info': {'attack': 8, 'defense': 4, 'magic': 3, 'difficulty': 4},
    #         'image': {
    #             'full': 'Aatrox.png',
    #             'sprite': 'champion0.png',
    #             'group': 'champion',
    #             'x': 0,
    #             'y': 0,
    #             'w': 48,
    #             'h': 48,
    #         },
    #         'tags': ['Fighter', 'Tank'],
    #         'partype': 'Blood Well',
    #         'stats': {
    #             'hp': 580,
    #             'hpperlevel': 90,
    #             'mp': 0,
    #             'mpperlevel': 0,
    #             'movespeed': 345,
    #             'armor': 38,
    #             'armorperlevel': 3.25,
    #             'spellblock': 32,
    #             'spellblockperlevel': 1.25,
    #             'attackrange': 175,
    #             'hpregen': 3,
    #             'hpregenperlevel': 1,
    #             'mpregen': 0,
    #             'mpregenperlevel': 0,
    #             'crit': 0,
    #             'critperlevel': 0,
    #             'attackdamage': 60,
    #             'attackdamageperlevel': 5,
    #             'attackspeedperlevel': 2.5,
    #             'attackspeed': 0.651,
    #         },
    #     }
    # }

    champions_data = {}

    for data in champions.values():
        champions_data[data['key']] = {
            'name': data['name'],
            # 'key': data['key'],
            'image': f'http://ddragon.leagueoflegends.com/cdn/{data["version"]}/img/champion/{data["image"]["full"]}',
        }
        # {
        #     '266': {'name': 'Aatrox', 'image': 'http://ddragon.leagueoflegends.com/cdn/11.7.1/img/champion/Aatrox.png'}
        # }

    return champions_data


class Tiltometer:
    def __init__(
        self, watcher, region, summoner_name, champions_data, number_of_games=10
    ):
        self.watcher = watcher
        self.region = region
        self.summoner_name = summoner_name
        self.number_of_games = number_of_games
        self.champions_data = champions_data

        try:
            self.summoner = self.get_summoner_data()
            self.account_id = self.summoner['accountId']
            self.matches = self.get_matches_data()

        except ApiError as err:

            error_message = (
                f'We should retry in {err.response.headers["Retry-After"]} seconds.\n'
                'This retry-after is handled by default by the RiotWatcher library, '
                'future requests wait until the retry-after time passes'
            )

            if err.response.status_code == 429:
                current_app.logger.error(error_message)
            else:
                raise Exception(err)

    def get_summoner_data(self):
        summoner = self.watcher.summoner.by_name(
            region=self.region,
            summoner_name=self.summoner_name,
        )
        # {
        #     'id': 'gBA29eZqQyLZ8NJfpVx3GvjCYI-wEMtefZ-Z8BRaN9I1Hsc',
        #     'accountId': '0hb0Q4rlLpQSS0mdyAH9jYfx1g7pSrsoP0vzGD4SreK8eVc',
        #     'puuid': 'oWc3se15FAhbd9YMZr24vvS3wBg3JdMA1mKIzKd5NfeVKNBEYVlkJYkdbRLs8hri8LmMIMPI3r6j2A',
        #     'name': 'BarreIs',
        #     'profileIconId': 3496,
        #     'revisionDate': 1617061508000,
        #     'summonerLevel': 466,
        # }
        return summoner

    def get_matches_data(self):
        return self.watcher.match.matchlist_by_account(
            region=self.region,
            encrypted_account_id=self.account_id,
            end_index=self.number_of_games,
        )['matches']
        # [
        #     {
        #         'platformId': 'EUW1',
        #         'gameId': 5184056143,
        #         'champion': 41,
        #         'queue': 440,
        #         'season': 13,
        #         'timestamp': 1617235832401,
        #         'role': 'SOLO',
        #         'lane': 'TOP',
        #     }
        # ]

    def get_stats_and_tilt(self):
        matches_stats = []
        number_of_wins = 0

        tilt_points = 50
        multiplier = 10
        cold_streak = 0

        for match_reference in self.matches:
            match = self.watcher.match.by_id(self.region, match_reference['gameId'])
            participant_identities = match['participantIdentities']

            participant_id = None
            for identity in participant_identities:
                if identity['player']['accountId'] == self.account_id:
                    participant_id = identity['participantId']
                    break

            if not participant_id:
                raise

            all_participants = match['participants']
            this_participant = all_participants[participant_id - 1]
            stats = this_participant['stats']

            if stats['participantId'] != participant_id:
                raise

            champion_id = this_participant['championId']

            kills = stats['kills']
            deaths = stats['deaths']
            assists = stats['assists']

            champion_img = self.champions_data[str(champion_id)]['image']
            position = match_reference['lane']

            pentakill = True if stats['pentaKills'] else False

            time = match['gameDuration']
            match_type = match['gameType']
            win = stats['win']
            number_of_wins += 1 if win else 0

            date = datetime.datetime.fromtimestamp(match_reference['timestamp'] / 1000)
            date = date.strftime('%d/%b %H:%M')

            match_stats_summary = {
                'kills': kills,
                'deaths': deaths,
                'assists': assists,
                'champion_name': self.champions_data[str(champion_id)]['name'],
                'champion_img': champion_img,
                'position': position,
                'pentakill': pentakill,
                'time': f'{int(time / 60)}:{str(time % 60).zfill(2)}',
                'match_type': match_type,
                'win': win,
                'date': date,
            }

            matches_stats.append(match_stats_summary)

            # When practising vs BOTS or custom games you never get tilted,
            # so they don't count. We even take 3 points off the tilt level,
            # since they are just for fun
            if match['gameMode'] != 'CLASSIC' or match['gameType'] != 'MATCHED_GAME':
                tilt_points -= 3
                continue

            if win:
                cold_streak = 0
                # you won the game, that should count for something right?
                tilt_points -= 5

                # if you won a game under 20 minutes probably means the
                # opponents forfited or you crushed them
                # multiplier for the more recent the game was
                if time < 1200:
                    tilt_points -= multiplier
            else:
                # 0.5 tilt points for every game lost
                # bigger multiplier the more recent the game was
                tilt_points += multiplier

                # add cold streak
                cold_streak += 1

                # if you lost a game under 20 minutes probably means you forfited
                # or you were crushed
                # multiplier for the more recent the game was
                if time < 1200:
                    tilt_points += multiplier

            # if you lost 2 or more games in a row you gain tilt points per game
            # bigger multiplier the more recent the cold strike was
            if cold_streak > 1:
                tilt_points += cold_streak * (multiplier)

            kda = (kills + assists) / max(1, deaths)

            # if your KDA is low... tilt points for you!
            if kda < 1:
                # tilt_points += 1.25 * multiplier
                tilt_points += 8
            elif kda < 2:
                # tilt_points += 0.75 * multiplier
                tilt_points += 3
            elif kda < 3:
                tilt_points += 1
            else:
                # if your kda is over 3 you did very well and you are happy
                # let's get some tilt point off of you ^^
                # tilt_points -= multiplier
                tilt_points -= 3

            multiplier -= 1

        if tilt_points > 100:
            tilt_points = 100
        elif tilt_points < 1:
            tilt_points = 0

        return matches_stats, number_of_wins, tilt_points

    def get_tilt(self):
        stats, number_of_wins, tilt_points = self.get_stats_and_tilt()

        response = {
            'status': 200,
            'wins': number_of_wins,
            'metadata': {
                # 'background': get_random_background_url(champions_dict),
                # 'display': get_random_display(),
            },
            'stats': stats,
            'summoner_name': self.summoner_name,
            'tilt_level': tilt_points,
        }
        return response
