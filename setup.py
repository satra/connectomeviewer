#!/usr/bin/env python
import sys
from glob import glob
from distutils import log
from distutils.cmd import Command
import numpy as np

# monkey-patch numpy distutils to use Cython instead of Pyrex
from build_helpers import generate_a_pyrex_source, package_check, make_cython_ext, INFO_VARS

from numpy.distutils.command.build_src import build_src
build_src.generate_a_pyrex_source = generate_a_pyrex_source

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)
    
    config.add_subpackage('cviewer')
    return config


################################################################################
# Dependency check
################################################################################

def _mayavi_version(pkg_name):
    from enthought.mayavi import version
    return version.version

def _traits_version(pkg_name):
    from enthought.traits import version
    return version.__version__

package_check('scipy', INFO_VARS['scipy_min_version'])
package_check('networkx', INFO_VARS['networkx_min_version'])
package_check('numpy', INFO_VARS['numpy_min_version'])
package_check('enthought.mayavi', INFO_VARS['mayavi_min_version'],version_getter=_mayavi_version)
package_check('enthought.traits', INFO_VARS['traits_min_version'],version_getter=_traits_version)

################################################################################
################################################################################
# For some commands, use setuptools

if len(set(('develop', 'bdist_egg', 'bdist_rpm', 'bdist', 'bdist_dumb', 
            'bdist_wininst', 'install_egg_info', 'egg_info', 'easy_install',
            )).intersection(sys.argv)) > 0:
    from setup_egg import extra_setuptools_args

# extra_setuptools_args can be defined from the line above, but it can
# also be defined here because setup.py has been exec'ed from
# setup_egg.py.
if not 'extra_setuptools_args' in globals():
    extra_setuptools_args = dict()
    
    
def main(**extra_args):
    from numpy.distutils.core import setup
    setup(
        name = 'ConnectomeViewer',
        version = INFO_VARS['version'],
        author = "Stephan Gerhard",
        author_email = "stephan.gerhard@epfl.ch",
        classifiers = [c.strip() for c in """\
            Development Status :: 4 - Beta
            Intended Audience :: Developers
            Intended Audience :: Science/Research
            Operating System :: OS Independent
            Operating System :: POSIX
            Operating System :: POSIX :: Linux 
            Operating System :: Unix
            Programming Language :: Python
            Topic :: Scientific/Engineering
            Topic :: Software Development
            """.splitlines() if len(c.split()) > 0],    
        description = "Multi-Modal MR Connectomics Framework for Analysis and Visualization",
        license = "Modified BSD License",
        long_description = INFO_VARS['long_description'],
        maintainer = 'Stephan Gerhard',
        maintainer_email = 'info@connectomics.org',
        platforms = ["Linux", "Unix"],
        url = 'http://www.connectomeviewer.org/',
        scripts = glob('scripts/*.py'),
        ext_modules = [per_ext, tvol_ext, rec_ext],         
        configuration = configuration,
        **extra_args
        )

    
if __name__ == "__main__":
    main()
