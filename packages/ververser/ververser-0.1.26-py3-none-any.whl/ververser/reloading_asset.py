from enum import Enum, auto
import logging
from typing import Any

from ververser.file_watcher import FileWatcher


logger = logging.getLogger(__name__)


class ReloadStatus( Enum ):
    NOT_CHANGED = auto()
    RELOADED = auto()
    FAILED = auto()


class ReloadingAsset:

    def __init__( self, f_load_asset, file_path ):
        self.f_load_asset = f_load_asset
        self.asset = None
        self.file_watcher = FileWatcher( file_path )
        self.reload_status = ReloadStatus.NOT_CHANGED
        self.reload()

    def __getattr__( self, name : str ) -> Any:
        return getattr( self.asset, name )

    def __bool__(self) -> bool:
        return bool( self.asset )

    def is_modified( self ) -> bool:
        return self.file_watcher.is_modified()

    def reload( self ) -> None:
        asset_path = self.file_watcher.file_path
        try:
            self.asset = self.f_load_asset( asset_path )
        except BaseException as e :
            logger.exception( f'Encountered an error during loading of asset from file "{asset_path}". Exception: {e}' )
            self.reload_status = ReloadStatus.FAILED
            self.asset = None
            return
        self.file_watcher.update()
        self.reload_status = ReloadStatus.RELOADED

    def update_watch( self ) -> None:
        self.file_watcher.update()

    def try_reload( self ):
        if self.is_modified():
            logger.info( f'File was modified! - {self.file_watcher.file_path} - Timestamp: {self.file_watcher.last_seen_time_modified}' )
            self.reload()
        else:
            self.reload_status = ReloadStatus.NOT_CHANGED
