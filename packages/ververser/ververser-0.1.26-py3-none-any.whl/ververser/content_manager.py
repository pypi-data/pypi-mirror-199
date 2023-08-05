from pathlib import Path
from typing import Any, Callable

from ververser.reloading_asset import ReloadingAsset, ReloadStatus
from ververser.entrypoint_wrapper import load_main_script, load_game_class, EntrypointWrapper
from ververser.multi_file_watcher import MultiFileWatcher
from ververser.script import load_script, Script

AssetLoaderType = Callable[ [ Path ], Any ]

EXPECTED_SCRIPT_EXTENSION = '.py'
EXPECTED_MAIN_SCRIPT_NAME = Path( 'vvs_main.py' )
EXPECTED_GAME_SCRIPT_NAME = Path( 'vvs_game.py' )


def is_script_path( path : Path ) -> bool:
    return path.suffix == EXPECTED_SCRIPT_EXTENSION


class ContentManager:

    """
    The asset manager works mainly on two categories of content:
    1) scripts
        When a single script is updated we will not try to do anything clever.
        We basically reinitialize the entire game to make sure all scripts are reloaded.
        In future versions of ververser we can always make this more intelligent.
        The game window is responsible for checking if it needs to reinitialize.
    2) non-scripts
        Non scripts can be anything, i.e. Meshes, Shader or Textures
        Reloading these, does not require reloading the entire game,
        We will just replace them while we keep running.

    Because scripts are dealt with separately,
    we will make a hard distinction between these two categories,
    and refer to non-script content as "assets".

    We also separate the step from checking whether files have been updated,
    from the step where they are actually reloaded.
    This is because depending on what kind of file has changed,
    a different type of reload might be performed.
    """

    def __init__( self, content_folder_path : Path ):
        self.content_folder_path = content_folder_path
        self.script_watcher = MultiFileWatcher( 'Script Watcher' )

        self.asset_loaders : list[ tuple[ str, AssetLoaderType ] ] = []
        self.reloading_assets : list[ ReloadingAsset ] = []

        self.is_any_asset_modified = False
        self.is_any_script_modified = False

    # ======== Generic functions ========

    def make_path_complete( self, content_path : Path ) -> Path:
        absolute_content_path = self.content_folder_path / content_path
        return absolute_content_path

    def exists( self, asset_path ) -> bool:
        complete_asset_path = self.make_path_complete( asset_path )
        return complete_asset_path.is_file()

    def update_watches( self ) -> None:
        for reloading_asset in self.reloading_assets:
            reloading_asset.update_watch()

        self.is_any_asset_modified = False
        for reloading_asset in self.reloading_assets:
            if reloading_asset.is_modified():
                self.is_any_asset_modified = True
                break

        self.script_watcher.update()
        self.is_any_script_modified = self.script_watcher.is_modified()

    # ======== Asset related functions ========

    def is_asset_path( self, content_path ) :
        for postfix, _ in reversed( self.asset_loaders ) :
            if str( content_path ).endswith( postfix ) :
                return True
        return False

    def load( self, content_path ) -> ReloadingAsset :
        absolute_asset_path = self.make_path_complete( content_path )
        asset_loader = self.get_asset_loader_for_file( absolute_asset_path )
        reloading_asset = ReloadingAsset(
            f_load_asset = asset_loader,
            file_path = absolute_asset_path
        )
        self.reloading_assets.append( reloading_asset )
        return reloading_asset

    def try_reload_assets( self ) -> ReloadStatus :
        overall_load_status = ReloadStatus.NOT_CHANGED
        for reloading_asset in self.reloading_assets :
            reload_status = reloading_asset.try_reload()
            if reload_status == ReloadStatus.RELOADED :
                overall_load_status = ReloadStatus.RELOADED
            if reload_status == ReloadStatus.FAILED :
                return ReloadStatus.FAILED
        return overall_load_status

    def register_asset_loader( self, postfix: str, f_load_asset: AssetLoaderType ) -> None :
        self.asset_loaders.append( (postfix, f_load_asset) )

    def get_asset_loader_for_file( self, file_path: Path ) -> AssetLoaderType :
        # reverse search through all registered loaders
        # this way. newest registered loaders overrule older ones
        for postfix, asset_loader in reversed( self.asset_loaders ) :
            if str( file_path ).endswith( postfix ) :
                return asset_loader
        raise KeyError( f'No asset loader found for file_path: "{file_path}". Known loaders: {self.asset_loaders}' )

    # ======== Script related functions ========

    def is_script_path( self, content_path ):
        return content_path.endswith( EXPECTED_SCRIPT_EXTENSION )

    def load_entrypoint_wrapper( self, game_window ) -> EntrypointWrapper:

        # first try to find a main script
        # otherwise try to find a game class

        entry_point_wrappers = {
            EXPECTED_MAIN_SCRIPT_NAME : load_main_script,
            EXPECTED_GAME_SCRIPT_NAME : load_game_class,
        }

        entrypoint_wrapper = None
        for wrapper_name, f_load in entry_point_wrappers.items():
            if self.exists( wrapper_name ) :
                absolute_entrypoint_path = self.make_path_complete( wrapper_name )
                self.script_watcher.add_file_watch( absolute_entrypoint_path )
                entrypoint_wrapper = f_load( absolute_entrypoint_path, game_window )
                break
        assert entrypoint_wrapper, 'Could not find entrypoints'
        return entrypoint_wrapper

    def load_script( self, script_path : Path, reinit_on_mod = True ) -> Script | ReloadingAsset:
        absolute_script_path = self.make_path_complete( script_path )
        if reinit_on_mod:
            return self._load_script( absolute_script_path )
        else:
            return self._load_script_as_asset( absolute_script_path )

    def _load_script( self, absolute_script_path : Path ):
        script = load_script( absolute_script_path )
        self.script_watcher.add_file_watch( absolute_script_path )
        return script

    def _load_script_as_asset( self, absolute_script_path ) -> ReloadingAsset:
        reloading_asset = ReloadingAsset(
            f_load_asset = load_script,
            file_path = absolute_script_path
        )
        self.reloading_assets.append( reloading_asset )
        return reloading_asset
