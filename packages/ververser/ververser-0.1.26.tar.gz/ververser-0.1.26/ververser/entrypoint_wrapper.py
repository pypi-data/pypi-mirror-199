from pathlib import Path
from runpy import run_path
from typing import Protocol


INIT_HOOK_NAME = 'vvs_init'
UPDATE_HOOK_NAME = 'vvs_update'
DRAW_HOOK_NAME = 'vvs_draw'
EXIT_HOOK_NAME = 'vvs_exit'


def invoke_if_not_none( f, *args, **kwargs ) -> None:
    if f:
        f( *args, **kwargs )


# We have two ways of wrapping a ververser app: using a script, or using a class

class EntrypointWrapper( Protocol ):

    def vvs_update( self, dt ) -> None:
        pass

    def vvs_draw( self ) -> None:
        pass

    def vvs_exit( self ) -> None:
        pass


class MainScript:

    def __init__( self, file_path : Path, game_window ):
        self.file_path = file_path
        self.data_module = run_path( str( file_path ) )

        self.vvs_init( game_window )

    def invoke_if_available( self, name, *args, **kwargs ) -> None:
        invoke_if_not_none( self.data_module.get( name ), *args, **kwargs )

    def vvs_init( self, game_window ) -> None:
        self.invoke_if_available( INIT_HOOK_NAME, game_window )

    def vvs_update( self, dt ) -> None:
        self.invoke_if_available( UPDATE_HOOK_NAME, dt )

    def vvs_draw( self ) -> None:
        self.invoke_if_available( DRAW_HOOK_NAME )

    def vvs_exit( self ) -> None:
        self.invoke_if_available( EXIT_HOOK_NAME )


def load_main_script( script_path : Path, game_window ) -> EntrypointWrapper:
    return MainScript( script_path, game_window )


EXPECTED_GAME_CLASS_NAME = 'VVSGame'


class GameClass:

    def __init__( self, file_path: Path, game_window ) :
        self.file_path = file_path
        self.data_module = run_path( str( file_path ) )

        Game = self.data_module.get( EXPECTED_GAME_CLASS_NAME )
        self.game = Game( game_window )

    def invoke_if_available( self, name, *args, **kwargs ) -> None:
        invoke_if_not_none( getattr( self.game, name, None ), *args, **kwargs )

    def vvs_update( self, dt ) -> None:
        self.invoke_if_available( UPDATE_HOOK_NAME, dt )

    def vvs_draw( self ) -> None:
        self.invoke_if_available( DRAW_HOOK_NAME )

    def vvs_exit( self ) -> None:
        self.invoke_if_available( EXIT_HOOK_NAME )


def load_game_class( script_path : Path, game_window ) -> EntrypointWrapper:
    return GameClass( script_path, game_window )



