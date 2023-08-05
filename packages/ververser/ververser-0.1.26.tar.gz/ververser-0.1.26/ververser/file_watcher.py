from enum import Enum, auto
import os.path
from pathlib import Path


class FileStatus( Enum ):
    NOT_CHANGED = auto()
    MODIFIED = auto()


class FileWatcher:

    def __init__( self, file_path: Path ):
        self.file_path = file_path
        self.last_seen_time_modified = self._get_time_modified()

    def _get_time_modified( self ) -> float:
        return os.path.getmtime( self.file_path )

    def update( self ) -> None:
        currently_seen_time_modified = self._get_time_modified()
        if currently_seen_time_modified > self.last_seen_time_modified:
            self.status = FileStatus.MODIFIED
        else:
            self.status = FileStatus.NOT_CHANGED
        self.last_seen_time_modified = currently_seen_time_modified

    def is_modified( self ) -> bool:
        return self.status == FileStatus.MODIFIED
