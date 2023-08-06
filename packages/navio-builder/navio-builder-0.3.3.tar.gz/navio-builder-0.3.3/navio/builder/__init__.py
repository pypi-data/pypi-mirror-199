'''
Lightweight Python Build Tool
'''

from ._nb import task
from ._nb import add_env
from ._nb import main
from ._nb import dump, pushd, zipdir
import pkgutil

try:
    import sh
    from ._nb import main, nsh
except ModuleNotFoundError:
    pass

__path__ = pkgutil.extend_path(__path__, __name__)

__all__ = [
    'task', 'main',
    'nsh', 'sh',
    'zipdir', 'add_env',
    'dump', 'dumps', 'pushd',
    'print_out', 'print_err'
]
