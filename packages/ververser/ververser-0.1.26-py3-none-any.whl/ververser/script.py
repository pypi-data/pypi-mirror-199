from pathlib import Path
from runpy import run_path


class Script:

    def __init__( self, file_path : Path ):
        self.file_path = file_path
        self.data_module = run_path( str( file_path ) )

    def __getattr__( self, name ):
        return self.data_module.get( name )


def load_script( script_path : Path ) -> Script:
    return Script( script_path )
