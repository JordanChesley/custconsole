"""
File containing all the raisable errors for
the custom console.
"""

__all__ = [
    'ArgumentError', 'CustConsoleException', 'DuplicateCommandError',
    'InvalidCommandParam', 'UnknownCommandError'
]


class CustConsoleException(Exception):
    """Base custconsole exception."""
    pass


class InfiniteStringError(CustConsoleException):
    """
    Raised when a console user passes in a string
    argument that is not properly closed, hence
    "infinite".
    """

    def __init__(self):
        super().__init__('String argument provided by user does not close')


class InvalidCommandParam(CustConsoleException):
    """
    Raised when the custom command being initiated
    has an invalid parameter passed to it.
    """

    def __init__(self, command, param, needed_type, passed_type):
        super().__init__(
            f'{command}\'s {param} parameter should be a {needed_type} type, not {passed_type} type')


class UnknownCommandError(CustConsoleException):
    """
    Raised when an unknown command is called to the
    console.
    """

    def __init__(self, command):
        super().__init__(
            f'\'{command}\' is not a command. Type \'help\' for a list of commands')


class DuplicateCommandError(CustConsoleException):
    """
    Raised when a custom command is defined more than
    once.
    """

    def __init__(self, command):
        super().__init__(
            f'Command \'{command}\' is defined more than once in the console script')


class ArgumentError(CustConsoleException):
    """
    Raised when too many or too little parameters
    are passed to the given function.
    """

    def __init__(self, function,  input_params, total_params):
        if input_params > total_params:
            msg = f'Too many arguments passed to \'{function.name}\''
        else:
            msg = f'More arguments need to be passed to \'{function.name}\''
        super().__init__(msg)
