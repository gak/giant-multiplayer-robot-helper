import arrow


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
