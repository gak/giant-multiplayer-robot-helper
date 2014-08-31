from __future__ import print_function
from glob import glob
import os
import time
import sys

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

        if not self.ensure_auth_key():
            return

        self.gmr = GMR(self.config)
        fun = getattr(self, self.config.command)
        fun()

    def ensure_auth_key(self):
        self.auth_key = AuthKey(self.config)
        if self.auth_key.ensure(self.ask_auth_key):
            return True

        print('Could not authenticate. Please try again')

    def ask_auth_key(self):
        print(
            'I will need your GMR auth key. '
            'You can find it at http://multiplayerrobot.com/Download'
        )
        return raw_input('Please enter your auth key: ')

    def print_game(self, game):
        print(game.name)
        for player in game.players:
            if game.current_turn.user_id == player.id:
                print('*', end='')
            else:
                print(' ', end='')

            if player.name:
                print('  ' + player.name)
            else:
                print('  ---')
        print()

    def games(self):
        gap = self.gmr.get_games_and_players()
        for game in gap.games:
            self.print_game(game)

    def play(self):
        gap = self.gmr.get_games_and_players()
        choices = {}
        choice = 0

        for game in gap.games:
            if game.current_turn.user_id != self.config.user_id:
                continue

            choice += 1
            choices[choice] = game

            print('{}: '.format(choice), end='')
            self.print_game(game)

        chosen = raw_input('Select game {}: '.format(choices.keys()))
        if not chosen:
            chosen = 1
        game = choices[int(chosen)]
        print(game)
        print('Downloading...')

        save_path = self.gmr.get_latest_save_file_bytes(game.id)
        print('Saved to {}'.format(save_path))

        print('Waiting for completed game...', end='')
        sys.stdout.flush()

        # TODO: Refactor with callback and maybe timeout
        glob_path = os.path.join(self.config.save_path, '*.Civ5Save')
        glob_path = os.path.expanduser(glob_path)
        original_files = set(glob(glob_path))
        new_save_path = None
        while True:
            time.sleep(1)

            # Callback
            print('.', end='')
            sys.stdout.flush()

            new_files = set(glob(glob_path))
            diff = new_files.difference(original_files)
            if not diff:
                continue

            new_save_path = list(diff)[0]
            break

        raw_input('\nFound {}.\nUpload? ctrl-c to abort: '.format(new_save_path))

        # TODO: Handle errors
        print(self.gmr.submit_turn(game.current_turn.turn_id, new_save_path))

