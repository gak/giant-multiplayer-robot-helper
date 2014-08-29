import json

from src.gmr import GMR


class AuthKey(object):
    def __init__(self, config):
        self.config = config

    def ensure(self, callback):
        self.load()
        if self.config.auth_key:
            return True

        self.config.auth_key = callback()

        self.config.user_id = self.authenticate()
        if self.config.user_id:
            self.save()
            return True

    def authenticate(self):
        gmr = GMR(self.config)
        return gmr.authenticate_user()

    def get_auth_path(self):
        return self.config.join('auth')

    def load(self):
        self.config.auth_key = None

        try:
            data = json.load(open(self.get_auth_path()))
            self.config.auth_key = data['auth_key']
            self.config.user_id = data['user_id']
        except IOError:
            return None

    def save(self):
        json.dump(
            {
                'auth_key': self.config.auth_key,
                'user_id': self.config.user_id,
            },
            open(self.get_auth_path(), 'w')
        )

