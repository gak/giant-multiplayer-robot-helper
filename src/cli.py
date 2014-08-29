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

        if not AuthKey(self.config).cli_ensure():
            return

        self.gmr = GMR(self.config)
        fun = getattr(self, self.config.command)
        fun()

    def games(self):
        print(self.gmr.get_games_and_players())

