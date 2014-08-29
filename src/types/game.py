from src.types.current_turn import CurrentTurn
from src.types.player import Player


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
