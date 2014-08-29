class Player(object):
    def __init__(self, player_db):
        self.name = None
        self.player_db = player_db

    def parse(self, data):
        '''
        We can either be parsing a player from the games list or the players
        list. The former will only give us a UserId and TurnOrder. The latter
        will give us a SteamID and some other useful fields like PersonaName.
        '''
        self.id = data.get('UserId') or data.get('SteamID')
        self.turn_order = data.get('TurnOrder')

        # Extras from "Players" response
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
