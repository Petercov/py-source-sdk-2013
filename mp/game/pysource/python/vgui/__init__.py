__all__ = ['controls']

from _vgui import *
from utils import ScreenWidth, ScreenHeight

def XRES(x): return int( x  * ( ScreenWidth() / 640.0 ) )
def YRES(y): return int( y  * ( ScreenHeight() / 480.0 ) )

# Aliases
DataType = DataType_t
