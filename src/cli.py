from src.config import Config

from src.gmr import GMR
from src.auth_key import AuthKey


class CLI(object):
    def __init__(self):
        self.gmr = None
        self.config = None
        self.auth_key = None

    def run(self):
        self.config = Config().parse()

        if not self.ensure_auth_key():
            return

        self.gmr = GMR(self.config)
        fun = getattr(self, self.config.command)
        fun()

    def ensure_auth_key(self):
        self.auth_key = AuthKey(self.config)
        if self.auth_key.ensure(self.ask_auth_key):
            return True

        print('Could not authenticate. Please try again')

    def ask_auth_key(self):
        print(
            'I will need your GMR auth key. '
            'You can find it at http://multiplayerrobot.com/Download'
        )
        return raw_input('Please enter your auth key: ')

    def games(self):
        gap = self.gmr.get_games_and_players()
        for game in gap.games:
            print(game)
            for player in game.players:
                print(player)

