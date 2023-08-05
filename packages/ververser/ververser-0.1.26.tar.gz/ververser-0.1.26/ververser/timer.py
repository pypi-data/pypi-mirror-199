from time import time


class Timer:

    def __init__(self):
        self.start = time()

    def get_elapsed_time( self ) -> float:
        now = time()
        return now - self.start

    def restart( self ) -> float:
        elapsed_time = self.get_elapsed_time()
        self.start = time()
        return elapsed_time
