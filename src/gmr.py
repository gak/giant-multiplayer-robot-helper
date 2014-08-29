import urlparse

import arrow

import requests
from shove import Shove


BASE_URL = 'http://multiplayerrobot.com/api/Diplomacy/'


class GMR(object):
    def __init__(self, config):
        self.config = config

        db_path = 'dbm://' + self.config.join('players')
        self.player_db = Shove(db_path)

    def _get(self, fragment, params=None):
        params = params or {}
        params['authKey'] = self.config.auth_key
        url = urlparse.urljoin(BASE_URL, fragment)
        return requests.get(url, params=params).json()

    def authenticate_user(self):
        return self._get('AuthenticateUser')

    def get_games_and_players(self, player_ids=None, retry_if_missing=True):
        player_ids = player_ids or []

        # Convert to str
        player_ids = [str(p) for p in player_ids]

        # Join as 123_234_345
        player_ids = '_'.join(player_ids)

        data = self._get('GetGamesAndPlayers', {
            'playerIDText': player_ids,
        })

        gap = GamesAndPlayers(self.player_db).parse(data)
        missing_players = gap.missing_player_ids()

        if missing_players and retry_if_missing:
            return self.get_games_and_players(
                player_ids=list(missing_players),
                retry_if_missing=False,
            )

        return gap


class GamesAndPlayers(object):
    def __init__(self, player_db):
        self.player_db = player_db

    def parse(self, data):
        pdb = self.player_db

        # Single values
        self.points = data.get('CurrentTotalPoints')

        # Arrays
        # Players before Games
        self.players = [Player(pdb).parse(p) for p in data.get('Players')]
        self.games = [Game(pdb).parse(g) for g in data.get('Games')]

        return self

    def missing_player_ids(self):
        missing = set()
        for game in self.games:
            for player in game.players:
                if player.has_extras():
                    continue
                if not player.id:
                    continue
                missing.add(player.id)

        return missing


class Game(object):
    def __init__(self, player_db):
        self.player_db = player_db

    def parse(self, data):
        pdb = self.player_db

        self.id = data.get('GameId')
        self.name = data.get('Name')
        self.current_turn = CurrentTurn().parse(data.get('CurrentTurn'))
        self.players = [Player(pdb).parse(p) for p in data.get('Players')]
        return self

    def __repr__(self):
        return 'Game #{} {}'.format(self.id, self.name)


class CurrentTurn(object):
    def parse(self, data):
        self.expires = data.get('Expires')
        self.is_first_turn = data.get('IsFirstTurn')
        self.number = data.get('Number')
        self.player_number = data.get('PlayerNumber')
        self.skipped = data.get('Skipped')
        self.started = arrow.get(data.get('Started'))
        self.turn_id = data.get('TurnId')
        self.user_id = data.get('UserId')
        return self


class Player(object):
    def __init__(self, player_db):
        self.name = None
        self.player_db = player_db

    def parse(self, data):
        self.id = data.get('UserId') or data.get('SteamID')
        self.turn_order = data.get('TurnOrder')

        # Extras
        self.name = data.get('PersonaName')
        self.state = data.get('PersonaState')
        self.avatar_url = data.get('AvatarUrl')

        # Save/Load from cache
        if self.has_extras():
            self.player_db[str(self.id)] = data
        else:
            cached = self.player_db.get(str(self.id))
            if cached:
                return self.parse(cached)

        return self

    def has_extras(self):
        return self.name

    def __repr__(self):
        return 'Player {}'.format(self.name)

