"""Simple Go lang iota pattern implementation"""

# This file is a part of iota package
# Licensed under Do-What-The-Fuck-You-Want license
# Initially made by @jedi2light (aka Carey Minaieva)

from .iota import iota

__pkg_name__ = 'pyiota'
__pkg_desc__ = 'Simple Go lang iota pattern implementation'
__project_license__ = 'WTFPL'
__author__ = '@jedi2light'
__author_email__ = 'jedi2light@jedi2light.moe'
__maintainer__ = __author__
__maintainer_email__ = __author_email__
__major_version__ = 1
__minor_version__ = 2
__patch_version__ = 1
__version_tuple__ = (__major_version__,
                     __minor_version__,
                     __patch_version__)
__version_string__ = '.'.join(list(map(str, __version_tuple__)))
