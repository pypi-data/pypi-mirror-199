print( f'Imported {__file__}' )


import math


def get_color_for_time( time ) -> tuple[ float, float, float ]:
    color = (
        0,
        0.25 + 0.25 * ( math.sin( time ) + 1 ),
        0.
    )
    return color