import argparse
import os


class Config(object):
    def __init__(self):
        self.config = None

    def parse(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            'command',
            help='Choose from setup, games, load, or upload.'
        )

        parser.add_argument(
            '-p', '--path',
            default='~/.gmr/',
            help='Path to config directory. Defaults to ~/.gmr/'
        )

        self.config = parser.parse_args()
        self.config.join = self.join
        self.ensure_directory()

        print(self.config)
        return self.config

    def ensure_directory(self):
        path = self.config.path = os.path.expanduser(self.config.path)
        if not os.path.exists(path):
            os.makedirs(path)

    def join(self, name):
        return os.path.join(self.config.path, name)

