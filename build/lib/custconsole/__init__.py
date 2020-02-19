"""
Create and customize your own console.

This module helps create the base of your console. This module
does not come with a pre-made run method. You must create/define
your own run method.

For more information on what custconsole provides, such as how to
define custom commands, how to invoke them, etc, please read the
README.md file.

For documentation, please visit [].

(C) 2020 Jordan Chesley
"""

# (c) Copyright 2020 Jordan Chesley
# License information found in LICENSE

from .custconsole import *
from .errors import *

__all__ = [
    '__title__', '__summary__', '__uri__', '__version__', '__author__',
    '__email__', '__license__', '__copyright__',
]


__copyright__ = 'Copyright 2020 Jordan Chesley'

__title__ = 'CustConsole'
__author__ = 'Jordan Chesley'
__email__ = 'jordan.r.chesley@gmail.com'
__version__ = '0.1.0'
__summary__ = ('Create a customizable console(s) for your program.')
__uri__ = 'https://github.com/JordanChesley/custconsole'
__license__ = 'MIT License'