import urlparse
import io

import requests
from shove import Shove

from src.types.games_and_players import GamesAndPlayers


BASE_URL = 'http://multiplayerrobot.com/api/Diplomacy/'


class GMR(object):
    def __init__(self, config):
        self.config = config

        db_path = 'dbm://' + self.config.join('players')
        self.player_db = Shove(db_path)

    def _get(self, fragment, params=None, raw_stream=False, payload=None):
        params = params or {}
        params['authKey'] = self.config.auth_key
        url = urlparse.urljoin(BASE_URL, fragment)

        kwargs = {}
        if raw_stream:
            kwargs['stream'] = True

        method = requests.get
        if payload:
            method = requests.post
            kwargs['data'] = payload

        request = method(url, params=params, **kwargs)

        if raw_stream:
            return request

        return request.json()

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

    def get_latest_save_file_bytes(self, game_id):
        stream = self._get('GetLatestSaveFileBytes', {
            'gameId': game_id,
        }, raw_stream=True)

        full_path = self.config.save_game_full_path()

        with open(full_path, 'wb') as fd:
            for chunk in stream.iter_content(io.DEFAULT_BUFFER_SIZE):
                fd.write(chunk)

        return full_path

    def submit_turn(self, turn_id, full_path):
        save_game = open(full_path, 'rb')

        return self._get('SubmitTurn', {
            'turnId': turn_id,
        }, payload=save_game)

