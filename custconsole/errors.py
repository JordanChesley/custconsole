"""
File containing all the raisable errors for
the custom console.
"""

__all__ = [
  'ArgumentError', 'BadLogoutCall', 'CustConsoleException', 'DuplicateCommandError',
  'InvalidCommandParam', 'NoUsersFile', 'UnknownCommandError'
]

class CustConsoleException(Exception):
  """Base custconsole exception."""
  pass

class NoUsersFile(CustConsoleException):
  """Raised when the ``users`` file cannot be found.
     in the same project directory as the console
     program.
  """
  __module__ = 'builtins'
  def __init__(self):
    super().__init__('Cannot find "users" file in the current project directory.')

class InvalidCommandParam(CustConsoleException):
  """Raised when the custom command being initiated
     has an invalid parameter passed to it."""
  __module__ = 'builtins'
  def __init__(self, command, param, nded_val, pssed_val):
    super().__init__(f'{command}\'s {param} parameter should be a {nded_val} type, not a {pssed_val}.')

class UnknownCommandError(CustConsoleException):
  """Raised when an unknown command is called to the
     console.
  """
  __module__ = 'builtins'
  def __init__(self, cmd):
    super().__init__(f'\'{cmd}\' is not a command. Type \'help\' for a list of commands.')

class DuplicateCommandError(CustConsoleException):
  """Raised when a custom command is defined more than
     once.
  """
  __module__='builtins'
  def __init__(self, command):
    super().__init__(f'Command \'{command}\' is defined more than once in the console script.')

class BadLogoutCall(CustConsoleException):
  """Raised when :meth:`custconsole.logout()` is unnecessarily called.
     This is most likely due to a scripting error."""
  __module__ = 'builtins'
  def __init__(self):
    super().__init__('custconsole.logout() was called when no user was logged in. Console will attempt to force quit.')

class ArgumentError(CustConsoleException):
  """Raised when too many or too little parameters
     are passed to the given function.
  """
  __module__ = 'builtins'
  def __init__(self, function,  input_params, total_params):
    if input_params > total_params:
      msg = f'Too many arguments passed to \'{function.name}\'.'
    else:
      msg = f'More arguments need to be passed to \'{function.name}\'.'
    super().__init__(msg)
