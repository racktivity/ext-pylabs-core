

import os.path
import sys
import os
import pkg_resources

UNIX_QBASE_PATH = "/opt/qbase5/"
# Dir cache
# Use to save dirs globally (prevent duplicate path generation)
dirs = dict()

def frozen():
    return hasattr(sys, 'frozen')

def platform_windows():
    return sys.platform.startswith('win')

def platform_linux():
    return sys.platform.startswith("linux")

def platform_sunos():
    return sys.platform.startswith("sunos")

def platform_darwin():
    return sys.platform.startswith('darwin')

class QbaseFinder(object):
    """Finds qbase path. Caches the path after first find."""
    def __init__(self):
        self._qbase = None

    def find(self):
        '''Find the base path of the PyMonkey sandbox installation'''
        if not self._qbase:
            # Give preference to user defined qbase
            if 'QBASE' in os.environ:
                 potential_qbase = os.environ['QBASE']
            # Added for the Q-Helper: the other qbase find algorithms fail
            # on py2exed scripts.
            elif frozen():
                # This PyMonkey has been py2exed
                # We will use the executable path to determine the qbase path
                potential_qbase = os.path.dirname(sys.executable)
            # Linux and Solaris have a default qbase path
            elif platform_linux() or platform_sunos():
                potential_qbase = UNIX_QBASE_PATH
            elif platform_darwin():
                potential_qbase = os.path.dirname(sys.path[0])
            elif platform_windows():
                # Need to autodetect
                # We assume python.exe is in qbase/Python25/
                # So we take the dirname of sys.executable (the python.exe)
                # and go one folder up (..)
                potential_qbase = os.path.abspath(
                    os.path.join(os.path.dirname(sys.executable), '..')
                )
            else:
                raise RuntimeError("Unsupported platform: %s" % (sys.platform, ))

            if not os.path.exists(os.path.join(potential_qbase, 'qshell')) \
                and not os.path.exists(os.path.join(potential_qbase, 'qshell.bat'))\
                and not os.path.exists(os.path.join(potential_qbase, 'qshell.exe')):
                raise RuntimeError('Unable to find Q-Shell executable in calculated baseDir %s, please export QBASE' % potential_qbase)

            self._qbase = potential_qbase

        return self._qbase

def fix_sys_path_win32():
    '''Fix sys.path on win32 systems.

    Add our version-independent site-packages to sys.path, and the PYMonkey
    installation directory (as a temporary fix).
    '''
    baseDir = find_qbase_path()
    # Setup dirs
    # frozen = py2exed
    if os.path.basename(sys.executable).startswith('python') or frozen():
        sys.path.append(os.path.join(baseDir, 'lib', 'pylabs', 'core'))
        sys.path.append(os.path.join(baseDir, 'lib', 'python', 'site-packages'))
        sys.path.append(os.path.join(baseDir, 'lib', 'python2.6', 'site-packages'))

def fix_sys_path_unix():
    '''Fix sys.path on unix systems.

    Add our version-independent site-packages to sys.path, and the PYMonkey
    installation directory (as a temporary fix).
    '''
    baseDir = find_qbase_path()
    # Setup dirs
    sys.path.append(os.path.join(baseDir, 'lib', 'pylabs', 'core'))
    sys.path.append(os.path.join(baseDir, 'lib', 'python', 'site-packages'))
    sys.path.append(os.path.join(baseDir, 'lib', 'python2.6', 'site-packages'))

def load_eggs():
    '''
    Load the pylabs egg and the site-packages eggs
    '''
    load_pylabs_egg()
    load_site_packages_eggs()

def find_eggs(path):
    """
    Helper for egg loader functions

    @param path: path to find the eggs on
    @type path: string
    @return: a list of eggs
    @rtype: list
    """
    eggs, errors = pkg_resources.working_set.find_plugins(
        pkg_resources.Environment([path])
    )
    return eggs

def load_pylabs_egg():
    """
    Load the PyMonkey egg, if there is one.

    If a PyMonkey egg is found, it is added to the end of sys.path. That way
    source PyMonkey distributions in a folder next to the egg(s) will be
    imported instead.
    """
    baseDir = find_qbase_path()
    # Egg dir is the normal pylabs core dir
    eggDir = os.path.join(baseDir, 'lib', 'pylabs', 'core')
    # Scan for pylabs eggs
    eggs = find_eggs(eggDir)
    # The eggs list will only contain the latest versions of the eggs it finds
    for egg in eggs:
        if egg.project_name.lower() == "pylabs":
            # We found the PyMonkey egg
            # Add it at the end of the python path so that pylabs sources
            # will be imported if present.
            sys.path.append(egg.location)
            # Nothing more to do
            return
    # No PyMonkey egg found, nothing we can do

def load_site_packages_eggs():
    """
    Load the eggs in the sandbox site packages folder.
    """
    baseDir = find_qbase_path()
    # Eggs should be in our own site-packages folder
    eggDir = os.path.join(baseDir, 'lib', 'python', 'site-packages')
    # Scan for pylabs eggs
    eggs = find_eggs(eggDir)
    # The eggs list will only contain the latest version of the eggs if finds
    for egg in eggs:
        # Add the egg in our path
        sys.path.append(egg.location)

def fix_sys_path():
    '''Fix sys.path per-platform.'''
    if platform_windows():
        fix_sys_path_win32()
    elif platform_linux() or platform_sunos():
        fix_sys_path_unix()

    load_eggs()

class Path(object):
    """Class for adding folders to environment path"""
    def __init__(self):
        path = os.environ['PATH']
        # Split the path into folders but filter out empty strings
        self._folders = [
            folder
            for folder in path.split(os.path.pathsep)
            if folder
        ]

    def add(self, folder):
        """Add folder to path. Will only be added if not in path yet!"""
        if folder not in self:
            self._folders.insert(0, folder)

    def commit(self):
        """Write changes to path to env"""
        os.environ['PATH'] = os.path.pathsep.join(self._folders)

    def __contains__(self, folder):
        if platform_windows():
            # Case insensitive
            newFolder = folder.lower()
            for oldFolder in self._folders:
                if oldFolder.lower() == newFolder:
                    return True
            return False

        # Case sensistive
        return folder in self._folders

def update_environ_path():
    """Add bin and other folders to environ path"""
    baseDir = find_qbase_path()
    path = Path()

    if platform_windows():
        # DLLs
        path.add(os.path.join(baseDir, 'lib', 'dll'))

    # Folder of the executable
    path.add(os.path.dirname(sys.executable))
    # Bin folder
    path.add(os.path.join(baseDir, "bin"))

    path.commit()

qbaseFinder = QbaseFinder()
def find_qbase_path():
   return qbaseFinder.find()

fix_sys_path()
#update_environ_path()


# install the apport exception handler if available
try:
    import apport_python_hook
except ImportError:
    pass
else:
    apport_python_hook.install()

