import os

from src.gmr import GMR


class AuthKey(object):
    def __init__(self, config):
        self.config = config

    def cli_ensure(self):
        self.config.auth_key = self.get_contents()
        if self.config.auth_key:
            return True

        print(
            'I will need your GMR auth key. '
            'You can find it at http://multiplayerrobot.com/Download'
        )
        self.config.auth_key = raw_input('Please enter your auth key: ')

        if self.test():
            self.save()
            return True

        print('Could not authenticate. Please try again...')

    def test(self):
        gmr = GMR(self.config)

        print('Testing...')
        return gmr.authenticate_user()

    def get_auth_key_path(self):
        return os.path.join(self.config.config, 'auth_key')

    def get_contents(self):
        try:
            return open(self.get_auth_key_path()).read().strip()
        except IOError:
            return None

    def save(self):
        open(self.get_auth_key_path(), 'wb').write(self.config.auth_key)

