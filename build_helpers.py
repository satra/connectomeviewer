''' Module with helper functions for cython building and package checking (derived from NiPy) '''

import sys
import os
from os.path import join as pjoin, dirname
import zipfile
import warnings
import shutil
from distutils.cmd import Command
from distutils.command.clean import clean
from distutils.version import LooseVersion
from distutils.dep_util import newer_group
from distutils.errors import DistutilsError
from distutils.extension import Extension

from numpy.distutils.misc_util import appendpath
from numpy.distutils import log

from distutils.command.clean import clean

# Get project related strings. Please do not change this line to use
# execfile because execfile is not available in Python 3
_info_fname = pjoin('cviewer', 'info.py')
INFO_VARS = {}
exec(open(_info_fname, 'rt').read(), {}, INFO_VARS)


# Sphinx import.
# from sphinx.setup_command import BuildDoc

DOC_BUILD_DIR = os.path.join('build', 'html')

################################################################################
# Distutils Command class for installing nipy to a temporary location. 
class TempInstall(Command):
    temp_install_dir = os.path.join('build', 'install')

    def run(self):
        """ build and install nipy in a temporary location. """
        install = self.distribution.get_command_obj('install')
        install.install_scripts = self.temp_install_dir
        install.install_base    = self.temp_install_dir
        install.install_platlib = self.temp_install_dir 
        install.install_purelib = self.temp_install_dir 
        install.install_data    = self.temp_install_dir 
        install.install_lib     = self.temp_install_dir 
        install.install_headers = self.temp_install_dir 
        install.run()

        # Horrible trick to reload nipy with our temporary instal
        for key in sys.modules.keys():
            if key.startswith('nipy'):
                sys.modules.pop(key, None)
        sys.path.append(os.path.abspath(self.temp_install_dir))
        # Pop the cwd
        sys.path.pop(0)
        import nipy

    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass


################################################################################
# Distutils Command class for API generation 
class APIDocs(TempInstall):
    description = \
    """generate API docs """

    user_options = [
        ('None', None, 'this command has no options'),
        ]


    def run(self):
        # First build the project and install it to a temporary location.
        TempInstall.run(self)
        os.chdir('doc')
        try:
            # We are running the API-building script via an
            # system call, but overriding the import path.
            toolsdir = os.path.abspath(pjoin('..', 'tools'))
            build_templates = pjoin(toolsdir, 'build_modref_templates.py')
            cmd = """%s -c 'import sys; sys.path.append("%s"); sys.path.append("%s"); execfile("%s", dict(__name__="__main__"))'""" \
                % (sys.executable, 
                   toolsdir,
                   self.temp_install_dir,
                   build_templates)
            os.system(cmd)
        finally:
            os.chdir('..')


################################################################################
# Code to copy the sphinx-generated html docs in the distribution.
def relative_path(filename):
    """ Return the relative path to the file, assuming the file is
        in the DOC_BUILD_DIR directory.
    """
    length = len(os.path.abspath(DOC_BUILD_DIR)) + 1
    return os.path.abspath(filename)[length:]


################################################################################

################################################################################
# Distutils Command class to clean
class Clean(clean):

    def run(self):
        clean.run(self)
        api_path = os.path.join('doc', 'api', 'generated')
        if os.path.exists(api_path):
            print "Removing %s" % api_path
            shutil.rmtree(api_path)
        if os.path.exists(DOC_BUILD_DIR):
            print "Removing %s" % DOC_BUILD_DIR 
            shutil.rmtree(DOC_BUILD_DIR)

# The command classes for distutils, used by the setup.py
cmdclass = {#'build_sphinx': MyBuildDoc,
#            'api_docs': APIDocs,
            'clean': Clean,
            }


# Dependency checks
def package_check(pkg_name, version=None,
                  optional=False,
                  checker=LooseVersion,
                  version_getter=None,
                  ):
    ''' Check if package `pkg_name` is present, and correct version

    Parameters
    ----------
    pkg_name : str
       name of package as imported into python
    version : {None, str}, optional
       minimum version of the package that we require. If None, we don't
       check the version.  Default is None
    optional : {False, True}, optional
       If False, raise error for absent package or wrong version;
       otherwise warn
    checker : callable, optional
       callable with which to return comparable thing from version
       string.  Default is ``distutils.version.LooseVersion``
    version_getter : {None, callable}:
       Callable that takes `pkg_name` as argument, and returns the
       package version string - as in::
       
          ``version = version_getter(pkg_name)``

       If None, equivalent to::

          mod = __import__(pkg_name); version = mod.__version__``
    '''
    if version_getter is None:
        def version_getter(pkg_name):
            mod = __import__(pkg_name)
            return mod.__version__
    try:
        mod = __import__(pkg_name)
    except ImportError:
        if not optional:
            raise RuntimeError('Cannot import package "%s" '
                               '- is it installed?' % pkg_name)
        log.warn('Missing optional package "%s"; '
                 'you may get run-time errors' % pkg_name)
        return
    if not version:
        return
    try:
        have_version = version_getter(pkg_name)
    except AttributeError:
        raise RuntimeError('Cannot find version for %s' % pkg_name)
    if checker(have_version) < checker(version):
        v_msg = 'You have version %s of package "%s"' \
            ' but we need version >= %s' % (
            have_version,
            pkg_name,
            version,
            )
        if optional:
            log.warn(v_msg + '; you may get run-time errors')
        else:
            raise RuntimeError(v_msg)


def generate_a_pyrex_source(self, base, ext_name, source, extension):
    ''' Monkey patch for numpy build_src.build_src method

    Uses Cython instead of Pyrex.

    Assumes Cython is present
    '''
    if self.inplace:
        target_dir = dirname(base)
    else:
        target_dir = appendpath(self.build_src, dirname(base))
    target_file = pjoin(target_dir, ext_name + '.c')
    depends = [source] + extension.depends
    # add distribution (package-wide) include directories, in order to
    # pick up needed .pxd files for cython compilation
    incl_dirs = extension.include_dirs[:]
    dist_incl_dirs = self.distribution.include_dirs
    if not dist_incl_dirs is None:
        incl_dirs += dist_incl_dirs
    if self.force or newer_group(depends, target_file, 'newer'):
        import Cython.Compiler.Main
        log.info("cythonc:> %s" % (target_file))
        self.mkpath(target_dir)
        options = Cython.Compiler.Main.CompilationOptions(
            defaults=Cython.Compiler.Main.default_options,
            include_path=incl_dirs,
            output_file=target_file)
        cython_result = Cython.Compiler.Main.compile(source,
                                                   options=options)
        if cython_result.num_errors != 0:
            raise DistutilsError("%d errors while compiling %r with Cython" \
                  % (cython_result.num_errors, source))
    return target_file


def make_cython_ext(modulename,
                    has_cython=True,
                    include_dirs=None,
                    extra_c_sources=None):
    ''' Create Cython extension builder from module names

    Returns extension for building and command class depending on
    whether you want to use Cython and ``.pyx`` files for building
    (`has_cython` == True) or the Cython-generated C files (`has_cython`
    == False).

    Assumes ``pyx`` or C file has the same path as that implied by
    modulename. 

    Parameters
    ----------
    modulename : string
       module name, relative to setup.py path, with python dot
       separators, e.g mypkg.mysubpkg.mymodule
    has_cython : bool, optional
       True if we have cython, False otherwise, default True
    include_dirs : None or sequence
       include directories
    extra_c_sources : None or sequence
       sequence of strings giving extra C source files

    Returns
    -------
    ext : extension object
    cmdclass : dict
       command class dictionary for setup.py

    Examples
    --------
    You will need Cython on your python path to run these tests. 
    
    >>> modulename = 'pkg.subpkg.mymodule'
    >>> ext, cmdclass = make_cython_ext(modulename, True, None,['test.c'])
    >>> ext.name == modulename
    True
    >>> pyx_src = os.path.join('pkg', 'subpkg', 'mymodule.pyx')
    >>> ext.sources == [pyx_src, 'test.c']
    True
    >>> import Cython.Distutils
    >>> cmdclass['build_ext'] == Cython.Distutils.build_ext
    True
    >>> ext, cmdclass = make_cython_ext(modulename, False, None, ['test.c'])
    >>> ext.name == modulename
    True
    >>> pyx_src = os.path.join('pkg', 'subpkg', 'mymodule.c')
    >>> ext.sources == [pyx_src, 'test.c']
    True
    >>> cmdclass
    {}
    '''
    if include_dirs is None:
        include_dirs = []
    if extra_c_sources is None:
        extra_c_sources = []
    if has_cython:
        src_ext = '.pyx'
    else:
        src_ext = '.c'
    pyx_src = pjoin(*modulename.split('.')) + src_ext
    sources = [pyx_src] + extra_c_sources
    ext = Extension(modulename, sources, include_dirs = include_dirs)
    if has_cython:
        from Cython.Distutils import build_ext
        cmdclass = {'build_ext': build_ext}
    else:
        cmdclass = {}
    return ext, cmdclass

