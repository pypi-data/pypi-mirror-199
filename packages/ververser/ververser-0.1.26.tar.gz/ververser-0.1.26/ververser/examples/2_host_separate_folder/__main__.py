import logging
from pathlib import Path
from ververser import GameWindow, set_global_game_window


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    game_window = GameWindow( content_folder_path = Path( __file__ ).parent / 'content' )
    set_global_game_window( game_window )
    game_window.run()
