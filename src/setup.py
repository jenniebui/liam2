from __future__ import print_function

import sys
from distutils.extension import Extension

from cx_Freeze import setup, Executable
from Cython.Distutils import build_ext
import numpy as np


# cython options

# Add the output directory of cython build_ext to sys.path so that build_exe
# finds and copies C extensions
class MyBuildExt(build_ext):
    def finalize_options(self):
        build_ext.finalize_options(self)
        sys.path.insert(0, self.build_lib)

ext_modules = [Extension("cpartition", ["cpartition.pyx"],
                         include_dirs=[np.get_include()]),
               Extension("cutils", ["cutils.pyx"],
                         include_dirs=[np.get_include()])
              ]
build_ext_options = {}


# cx_freeze options
build_exe_options = {
    # compress zip archive
    "compressed": True,
    # optimize pyc files (strip docstrings and asserts)
    "optimize": 2,
    # strip paths in __file__ attributes
    "replace_paths": [("*", "")],
    #"includes": ["matplotlib.backends.backend_qt4agg"],
    "includes": ["matplotlib.backends.backend_tkagg"],
    "namespace_packages": ["mpl_toolkits"],
    "excludes": [
        # linux-specific modules
        "_codecs", "_codecs_cn", "_codecs_hk", "_codecs_iso2022",
        "_codecs_jp", "_codecs_kr", "_codecs_tw",
        # common modules
        "Cython", "_ssl",
        "base64", "bz2", "compiler",
        "doctest", "dummy_thread",
        "dummy_threading", "email", "ftplib",
        "logging", "multiprocessing", "nose",
        "numpy.distutils", "numpy.core._dotblas",
        "os2emxpath", "pdb", "pkg_resources",
        "posixpath", "pydoc", "pydoc_topics", "repr", "scipy",
        "select", "stringprep", "strptime",
        "tcl", "xml"

        # matplotlib => calendar, distutils, unicodedata
        # matplotlib.backends.backend_tkagg => Tkconstants, Tkinter
        # ctypes, io are required now
    ]
}

setup(name="liam2",
      version="0.8.0",
      description="LIAM2",

      cmdclass={"build_ext": MyBuildExt},
      ext_modules=ext_modules,

      options={"build_ext": build_ext_options,
               "build_exe": build_exe_options},
      executables=[Executable("main.py")],
      requires=['numpy', 'numexpr', 'tables', 'carray'])
