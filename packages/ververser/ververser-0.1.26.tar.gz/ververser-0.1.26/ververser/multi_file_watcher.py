import logging
from pathlib import Path
from ververser.file_watcher import FileWatcher, FileStatus


logger = logging.getLogger( __name__ )


class MultiFileWatcher :

    def __init__( self, name: str = "<not set>" ) :
        self.name = name
        self.file_watchers: list[ FileWatcher ] = [ ]
        self.status = FileStatus.NOT_CHANGED

    def add_file_watch( self, file_path: Path ) -> None :
        self.file_watchers.append( FileWatcher( file_path ) )

    def clear( self ) -> None :
        self.file_watchers = [ ]

    def update( self ) -> None:
        for file_watcher in self.file_watchers:
            file_watcher.update()

        for file_watcher in self.file_watchers:
            if file_watcher.status == FileStatus.MODIFIED:
                self.status = FileStatus.MODIFIED
                return
        self.status = FileStatus.NOT_CHANGED

    def is_modified( self ) -> bool:
        return self.status == FileStatus.MODIFIED
