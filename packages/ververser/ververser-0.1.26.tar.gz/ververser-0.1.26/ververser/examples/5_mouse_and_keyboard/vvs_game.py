import logging
from pyglet.gl import glClearColor
import pyglet.window.key as key
from ververser import GameWindow, host_this_folder
import numpy as np


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    host_this_folder()


Color = tuple[ float, float, float ]


class VVSGame:

    def __init__( self, game_window : GameWindow ):
        self.game_window = game_window
        self.total_time = 0

    def vvs_update( self, dt ):
        if self.game_window.keyboard.is_down( key.SPACE ):
            color = self._use_mouse_for_color()
        else:
            color = self._use_keyboard_for_color()
        glClearColor( color[0], color[1], color[2], 1.0 )

    def _use_mouse_for_color( self ) -> Color:
        mouse_pos = self.game_window.mouse.get_position()
        size = self.game_window.size
        cx = mouse_pos[0] / size[0]
        cy = mouse_pos[1] / size[1]
        return ( cx, cy, 0. )

    def _use_keyboard_for_color( self ) -> Color:
        color = ( 0., 0., 0. )
        color_per_key = [
            ( key.UP, ( 1., 0., 0. ) ),
            ( key.DOWN, ( 0., 1., 0. ) ),
            ( key.LEFT, ( 0., 0., 1. ) ),
            ( key.RIGHT, ( 0.5, 0.5, 0.5 ) ),
        ]
        for keyboard_key, keyboard_color in color_per_key :
            if self.game_window.keyboard.is_down( keyboard_key ) :
                color = np.add( color, keyboard_color )
        return color
