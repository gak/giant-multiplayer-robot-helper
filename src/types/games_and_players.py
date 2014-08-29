from src.types.game import Game
from src.types.player import Player


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
