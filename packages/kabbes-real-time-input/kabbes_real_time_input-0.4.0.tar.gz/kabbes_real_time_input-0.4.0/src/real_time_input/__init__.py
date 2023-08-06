import os
import platform
import dir_ops as do

_Dir = do.Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 

KEY_MAPPING = {
  'Windows': {
    '\r': 'ENTER', #all values need to be longer than one character to not confuse with an input
    '\t': 'TAB',
    '\x08': 'BACKSPACE'
  },
  'Linux': {
    '\n': 'ENTER',
    '\t': 'TAB',
    '\x7f': 'BACKSPACE',
    '\x1b': 'ESCAPE'
  }
}

# First, see what kind of platform we are running on
PLATFORM_SYSTEM = platform.system()
if PLATFORM_SYSTEM == 'Darwin' or PLATFORM_SYSTEM == 'Linux': # Linux and Mac behave the same
    PLATFORM_SYSTEM = 'Linux'
    import termios
    import tty

elif PLATFORM_SYSTEM == 'Windows':
    import msvcrt

from .RealTimeInput import RealTimeInput
from .Client import Client
