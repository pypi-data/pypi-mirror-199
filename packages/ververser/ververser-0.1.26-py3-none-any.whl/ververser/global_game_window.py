from typing import Optional, Any

from ververser.game_window import GameWindow


_GAME_WINDOW = Optional[ Any ]


def get_global_game_window() -> GameWindow:
    assert _GAME_WINDOW, 'Global game window not set'
    return _GAME_WINDOW


def set_global_game_window( game_window : GameWindow ) -> None:
    global _GAME_WINDOW
    _GAME_WINDOW = game_window
