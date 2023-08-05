import inspect
from pathlib import Path
from ververser.game_window import GameWindow
from ververser.global_game_window import set_global_game_window


def make_game_window( content_folder_path : Path ) -> GameWindow:
    return GameWindow( content_folder_path = content_folder_path )


def host_this_folder( f_make_window = make_game_window, n_frames_back = 1 ) -> None:
    # Determine the path of the file in which we invoked this function
    call_site_frame_info = inspect.stack()[ n_frames_back ]
    call_site_frame = call_site_frame_info[ 0 ]
    call_site_module = inspect.getmodule( call_site_frame )
    call_site_module_path = call_site_module.__file__
    call_site_folder_path = Path( call_site_module_path ).parent

    # Run the game, using the invocation folder as entrypoint
    game_window = f_make_window( call_site_folder_path )
    set_global_game_window( game_window )
    game_window.run()
