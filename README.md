giant-multiplayer-robot-helper
==============================

A simple command line interface for http://multiplayerrobot.com/

**NOTE** I don't really use this any more, but as far as I'm aware it is still working just as I left it--at least until GMR release their new website.

Installation
---------------------------

Some python is required to be installed.

Run `pip install -r requirements.txt` to install required libraries.

Usage
-----

**./gmr games**

Lists all games you're currently in, with player names.

**./gmr play**

Show a list of games where it's your turn, then when selecting one, it will download the save file to the default location in Linux.

It will wait for you to play your turn and detect a new save game in the hotseat save game directory, and ask for you to submit.


