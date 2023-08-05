from ververser.global_game_window import get_global_game_window
from ververser.script import Script
from ververser.reloading_asset import ReloadingAsset


def import_script( script_path : str, reinit_on_mod = True ) -> Script | ReloadingAsset:
    return get_global_game_window().content_manager.load_script( script_path, reinit_on_mod = reinit_on_mod )
