from copy import deepcopy
from pyglet.window.mouse import MouseStateHandler


class Mouse:

    def __init__( self ):
        self._previous_mouse_state = MouseStateHandler()
        self._current_mouse_state = MouseStateHandler()

    def get_handler( self ) -> MouseStateHandler:
        return self._current_mouse_state

    def update( self ) -> None:
        self._previous_key_states = deepcopy( self._current_mouse_state )

    def is_down( self, key ) -> bool:
        return self._current_mouse_state[ key ]

    def is_up( self, key ) -> bool:
        return not self._current_mouse_state[ key ]

    def is_pressed( self, key ) -> bool:
        current_is_down = self._current_mouse_state[ key ]
        previous_is_down = self._previous_mouse_state[ key ]
        return current_is_down and not previous_is_down

    def is_released( self, key ) -> bool:
        current_is_down = self._current_mouse_state[ key ]
        previous_is_down = self._previous_mouse_state[ key ]
        return not current_is_down and previous_is_down

    def get_position( self ) -> tuple[ float, float ]:
        return ( self._current_mouse_state[ 'x' ], self._current_mouse_state[ 'y' ] )
