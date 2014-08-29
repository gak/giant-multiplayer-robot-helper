import urlparse

import requests


BASE_URL = 'http://multiplayerrobot.com/api/Diplomacy/'


class GMR(object):
    def __init__(self, config):
        self.config = config

    def _get(self, fragment, params=None):
        params = params or {}
        params['authKey'] = self.config.auth_key
        url = urlparse.urljoin(BASE_URL, fragment)
        return requests.get(url, params=params).json()

    def authenticate_user(self):
        return self._get('AuthenticateUser')

    def get_games_and_players(self, player_ids=None):
        player_ids = player_ids or []
        return self._get('GetGamesAndPlayers', {
            'playerIDText': '_'.join(player_ids),
        })

