from distutils.core import setup
import py2exe
import sys
from distutils.core import setup
from glob import glob
import VERSION

# Workaround to get all them encodings
def get_required_encodings():
    import encodings
    import os

    imports = []
    for path in encodings.__path__:
        for filename in os.listdir(path):
            if filename.endswith(".py"):
                import_name = filename[:-3]
                if import_name != "__init__":
                    imports.append("encodings.%s" % import_name)
    return imports

# The next lines are shamelessly borrowed from http://www.py2exe.org/index.cgi/win32com.shell
# ...
# ModuleFinder can't handle runtime changes to __path__, but win32com uses them
try:
    # py2exe 0.6.4 introduced a replacement modulefinder.
    # This means we have to add package paths there, not to the built-in
    # one.  If this new modulefinder gets integrated into Python, then
    # we might be able to revert this some day.
    # if this doesn't work, try import modulefinder
    try:
        import py2exe.mf as modulefinder
    except ImportError:
        import modulefinder
    import win32com, sys
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    MISSING = "win32com.shell"
    __import__(MISSING)
    m = sys.modules[MISSING]
    for p in m.__path__[1:]:
        modulefinder.AddPackagePath(MISSING, p)
except ImportError:
    # no build path setup, no worries.
    pass

# END BORROWED LINES


icon_path = "resources/example.ico"
build_dict = {
              "name": "Example",
              "version": VERSION.version,
              "description": "Example: check out sweet MD5s and websites",
              "windows": [ {"script" : "example.py",
                             "icon_resources" : [(1, icon_path)] }],
              # These lines may need to change depending on your Visual Studio installation
              "data_files": [("resources", [icon_path]),
                                             ("Microsoft.VC90.CRT", 
                                              glob(r'C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))],
              "options": {'py2exe': {
                                        "bundle_files": 1,
                                        "includes":  get_required_encodings(),
                                        'excludes': ["Tkinter", "Tkconstants", "tcl" ],
                                        'dll_excludes': [ "mswsock.dll", "powrprof.dll" ],
                                        'ascii': True,
                                     }
                          },
              "zipfile": None
             }
    

setup(**build_dict)
