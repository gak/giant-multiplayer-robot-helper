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

        parser.add_argument(
            '-s', '--save-path',
            default='~/.local/share/Aspyr/Sid Meier\'s Civilization 5/'
                    'Saves/hotseat/',
        )

        parser.add_argument(
            '-f', '--save-file-name',
            default='(GMR) Play this one!.Civ5Save',
        )

        self.config = parser.parse_args()
        self.config.join = self.join
        self.config.save_game_full_path = self.save_game_full_path
        self.ensure_directory()

        return self.config

    def ensure_directory(self):
        path = self.config.path = os.path.expanduser(self.config.path)
        if not os.path.exists(path):
            os.makedirs(path)

    # These are tacked onto the returned config object in parse()

    def join(self, name):
        return os.path.join(self.config.path, name)

    def save_game_full_path(self):
        return os.path.expanduser(os.path.join(
            self.config.save_path,
            self.config.save_file_name,
        ))
