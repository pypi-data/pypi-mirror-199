__all__ = ['packages']
import sys
import os
import inspect
from runpy import run_module


def packages():
    """
    Import any packages defined in the requirements.txt file
    """
    _files = [
        i.filename
        for i in inspect.getouterframes(inspect.currentframe())
        if not str(i.filename).startswith('<frozen') and str(i.filename).endswith('.py')
    ]
    _importer_dir = os.path.dirname(_files[-1]) if len(_files) > 0 else None
    if _importer_dir:
        _requirement_file = os.path.join(_importer_dir, 'requirements.txt')
        if os.path.exists(_requirement_file):
            _packages_dir = os.path.join(_importer_dir, '__pypackages__')
            if os.path.exists(_packages_dir) and os.path.getmtime(_requirement_file) > os.path.getmtime(_packages_dir):
                for root, dirs, files in os.walk(_packages_dir, topdown=False):
                    for file_name in files:
                        os.remove(os.path.join(root, file_name))
                    for dir_name in dirs:
                        os.rmdir(os.path.join(root, dir_name))
                    os.rmdir(_packages_dir)
            if not os.path.exists(_packages_dir):
                os.mkdir(_packages_dir)
                _old_exit = sys.exit
                _old_argv = list(sys.argv)
                _old_path = list(sys.path)
                sys.exit = lambda x: {}
                sys.argv = ['pip', 'install', '--no-cache-dir', '--disable-pip-version-check', '--upgrade', '--target', _packages_dir, '--requirement', _requirement_file]
                run_module('pip', run_name='__main__', alter_sys=True)
                sys.argv = _old_argv
                sys.exit = _old_exit
                sys.path = _old_path
            if _packages_dir not in sys.path:
                sys.path.insert(1, _packages_dir)
