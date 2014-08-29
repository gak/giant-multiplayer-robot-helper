import os

from src.gmr import GMR


class AuthKey(object):
    def __init__(self, config):
        self.config = config

    def ensure(self, callback):
        self.config.auth_key = self.get_contents()
        if self.config.auth_key:
            return True

        self.config.auth_key = callback()

        if self.test():
            self.save()
            return True

    def test(self):
        gmr = GMR(self.config)
        return gmr.authenticate_user()

    def get_auth_key_path(self):
        return self.config.join('auth_key')

    def get_contents(self):
        try:
            return open(self.get_auth_key_path()).read().strip()
        except IOError:
            return None

    def save(self):
        open(self.get_auth_key_path(), 'wb').write(self.config.auth_key)

