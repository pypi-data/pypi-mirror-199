import logging
from ververser import GameWindow, host_this_folder
from pyglet.gl import glClearColor


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    host_this_folder()


def vvs_init( game_window : GameWindow ):
    glClearColor( 0, 1, 0, 1.0 )
