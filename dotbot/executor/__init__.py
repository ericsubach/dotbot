from .executor import Executor
from .linker import Linker
from .cleaner import Cleaner
from .commandrunner import CommandRunner

# Windows 7 support.
import os
if os.name == 'nt':
    try:
        from .linker_windows import LinkerWindows7
        from .cleaner_windows import CleanerWindows7
    except ImportError: # TODO need correct error type for missing requirement
        exit('The python library "win32file" must be installed for this program to work on Windows.')
