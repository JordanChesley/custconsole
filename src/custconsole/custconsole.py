"""
The main package file containing the necessary methods
to run the custom console.
"""

__all__ = ['Command', 'custconsole']

from .errors import InvalidCommandParam, UnknownCommandError, DuplicateCommandError, ArgumentError, InfiniteStringError


class custconsole():
    """
    Creates an instance of the custom CLI.

    Parameters
    ----------
    name: Optional[:class:`str`]
        The name of the console. This is defaults to 'Custom
        Console'.

    version: Optional[:class:`str`]
        The version number of your console. This number should
        be regularly updated in relevance to the amount of
        updates you've implemented. Defaults to '1.0.0'.

    prompt: Optional[:class:`str`]
        The prompt shown when the console requests a command.
        Defaults to '> '.
    """

    def __init__(self, **attrs):
        self.name = attrs.get('name') if 'name' in attrs else 'Custom Console'
        self.version = attrs.get('version') if 'version' in attrs else '1.0.0'
        self.prompt = attrs.get('prompt') if 'prompt' in attrs else '> '

        # Let's format the console header. Always include the following line:
        self.header = f'{self.name} v[{self.version}]'

        # Always include and finish with this statement:
        self.header += '\nType \'help\' for a list of commands.'

        self.commands = {}
        self.visible_commands = {}

    def set_prompt(self, prompt):
        self.prompt = prompt

    def run(self):
        """
        Runs the console application. Ends when 'exit' or 'quit'
        is called by the user.
        """
        while True:
            try:
                print('')
                command_string = input(self.prompt)
                command, args, kwargs = self._parse(command_string)
                if command == 'exit' or command == 'quit':
                    exit()
                self.invoke(command_string)
            except KeyboardInterrupt:
                continue
            except Exception as e:
                print(e)

    def help(self, all=False):
        """
        Print a list of commands defined in the console.

        Parameters
        ----------
        all: :class:`bool`
          If True, lists all commands defined in the console,
          including hidden commands. Defaults to False.
        """
        cmdList = self.commands if all else self.visible_commands
        for command in cmdList:
            command = cmdList[command]
            name = command.name.ljust(20)
            desc = command.description
            print(name, desc)

    def _add_command(self, command, hidden):
        """
        Adds a command to the console's command list.
        This should never be called manually.

        Parameters
        ----------
        command: :class:`.Command`
            The command that's being added. Must be formatted
            with the 'Command' class. 

        Raises
        ------
        DuplicateCommandError
            Raised when more than one instance of a command is
            created.
        """

        if command.name in self.commands:
            raise DuplicateCommandError(command.name)
        self.commands[command.name] = command
        if not hidden:
            self.visible_commands[command.name] = command

        # We order our commands in alphabetical order so that
        # users can easily locate the command in the help list.
        self.commands = self._sort_commands(self.commands)
        self.visible_commands = self._sort_commands(self.visible_commands)

    def remove_command(self, command):
        """
        Removes a command from the console's command list.

        Parameters
        ----------
        command: :class:`str`
            Name of the command to be removed.

        Raises
        ------
        UnknownCommandError
            Raised when the given command doesn't exist in
            the internal command list.
        """

        try:
            self.commands.pop(command)
            self.visible_commands.pop(command)
        except KeyError:
            raise UnknownCommandError(command)

    def _sort_commands(self, command_list):
        """
        We use this function to list our commands in alphabetical
        order. This should never be called manually.

        Parameters
        ----------
        command_list: :class:`dict`
            This is the command list holding the custom commands.
            This is normally custconsole.commands.
        """

        ordered_list = {}
        i = 0
        keys = sorted(command_list)
        for _ in range(len(command_list)):
            ordered_list[keys[i]] = command_list[keys[i]]
            i += 1
        return ordered_list

    def _parse(self, command_string):
        """
        Parse the given command into the command name, arguments,
        and keyword arguments. This function is called by the
        :meth:`custconsole.invoke()` function and should not be
        called manually.

        Parameters
        ----------
        command_string: :class:`str`
            This is the string passed into custconsole.invoke().
            This is normally the console user's input.

        Returns
        -------
        :class:`str`
            The name of the command, but not the actual command instance.

        :class:`list`
            List of arguments (not keyword arguments) to be passed to the
            command.

        :class:`dict`
            Dictionary of keyword arguments to be passed to the command.

        Raises
        ------
        InfiniteStringError
            Raised if parser detects a string argument that does not close.
        """
        command_string = command_string + ' '

        # Separate the command and the parameters.
        cmd, pars = command_string.split(' ', maxsplit=1)
        args = []
        kwargs = {}
        detecting_keyword = False
        variable_name = None

        # Run continuously until the 'pars' variable is empty.
        while pars != '':
            for char in pars:

                # An '=' signals a keyword argument exists. We find the
                # name before the '=' and have toggle the value detector
                # so that we can assign it the the kwarg.
                if char == '=':
                    split = pars.find(char)
                    variable_name = pars[0:split]
                    pars = pars.replace(variable_name + '=', '', 1)
                    detecting_keyword = True
                    break

                # A "'" signals a string exists. We find the other "'" and
                # take the value between and save it to our args list.
                elif char == '\'' or char == '\"':
                    start = pars.find(char)
                    print(pars[start:])

                    # We need to offset the start of the string by oneso that
                    # we can find the ending ' character
                    end = pars[start+1:].find(char)

                    # If the string does not end, throw an exception
                    if end == -1:
                        raise InfiniteStringError()

                    # The ending index is offset by two because:
                    # 1. We need to correct for the start index's offset (one).
                    # 2. We need to add one so that we actually catch the ' at
                    #    the end of the string.
                    end = end + 2
                    if detecting_keyword:
                        kwargs[variable_name] = pars[start+1:end-1]
                        print(f'{variable_name}={kwargs[variable_name]}')
                        detecting_keyword = False
                    else:
                        args.append(pars[start+1:end-1])
                        print(f'Arg string: {pars[start+1:end-1]}')
                    pars = pars.replace(pars[start:end], '', 1)
                    if pars[0] == ' ':
                        pars = pars.replace(' ', '', 1)
                    break

                # a ' ' signals that we've passed a single-word argument.
                # We go back and grab the value, and save it to our args list.
                elif char == ' ':
                    end = pars.find(char)
                    if pars[:end] != ' ':
                        if detecting_keyword:
                            kwargs[variable_name] = pars[:end]
                            print(f'{variable_name}={kwargs[variable_name]}')
                            detecting_keyword = False
                        else:
                            args.append(pars[:end])
                    pars = pars.replace(pars[:end + 1], '', 1)
                    break
        print(f'Args: {args}')
        print(f'kwargs: {kwargs}')
        return cmd, args, kwargs

    def invoke(self, command_string):
        """
        Parses the given string and invokes the command parsed,
        passing in the given arguments.

        Parameters
        ----------
        command_string: :class:`str`
            The command and any parameters passed into the command.

        Raises
        ------
        UnknownCommandError
            Raised when the user calls for a command not found in the
            internal command list.

        ArgumentError
            Raised when too many or too little arguments are given to
            run the requested command.
        """

        # custconsole._parse() returns 3 objects so we assign
        # three variables to the method.
        command_string = command_string.lstrip().rstrip()

        if len(command_string) > 1:
            command, args, kwargs = self._parse(command_string)
        else:
            command, args, kwargs = command_string, [], {}

        # If the user doesn't define a 'help' command, we still want
        # a help message to appear when it's called. So, we can use
        # our own call here. If they do have a 'help' command, we
        # will use that one instead.
        if command == 'help':
            if 'help' not in self.commands:
                self.help()

                # We call return simply because we have no reason to
                # continue to the rest of the method.
                return

        # The command may not exist; if not we throw an error.
        if command not in self.commands:
            raise UnknownCommandError(command)

        command = self.commands[command]
        try:
            command.callback(*args, *kwargs)

        # We may get an error because the user did not pass enough
        # arguments to the method. We want to detect this and act
        # so we can inform the user of what happened.
        except TypeError as e:
            if 'positional' and 'argument' in str(e):
                errmsg = str(e).split()
                raise ArgumentError(command, errmsg[6], errmsg[2])

    def command(self, name=None, hidden=False, **kwargs):
        """
        A decorator used to define custom commands for your console.
        Optional arguments that are passed through the decorator all
        override the values offered by the callabck function.

        Parameters
        ----------
        name: Optional[:class:`str`]
            Name of the command. Defaults to function name.

        description: Optional[:class:`str`]
            Command's description. Defaults to function's docstring,
            if provided. Otherwise, defaults to 'No description provided.'

        hidden: Optional[:class:`bool`]
            Decides if the command should be hidden in the help list. True
            means this command will not be shown in the help list. False
            means it will be shown. Defaults to False.

        Example
        -------
        .. code-block:: python

            cc = custconsole.custconsole()

            @cc.command()
            def hello():
                print('world!')
            # Command{name: 'hello', description: 'No description provided.', hidden: False}

            @cc.command(name='repeat', description='Echos given statement.', hidden=True)
            def echo(*phrase):
                print(*phrase)
            # Command{name: 'repeat', description: 'Echos given statement.', hidden: True}


        """

        def decorate(func):
            result = Command(func, name=name, **kwargs)
            self._add_command(result, hidden)
            return result

        return decorate


class Command():
    """
    Class used to identify, format, and modify the custom console's
    commands. This class is called automatically by the command
    decorator and should not be manually called.

    Parameters
    ----------
    func: :class:`func`
        The function being created into a command. This is passed
        so that the function can be called when the user calls it
        in the command line.

    name: Optional[:class:`str`]
        The name/alias of the command. This is the name typed into
        the console by the user, e.g. 'test'. This name is defaulted
        to the function name.

    description: Optional[:class:`str`]
        The description of the command. This is the description]
        provided in the 'help' command. This parameter is defaulted
        to the function's docstring. If the docstring is not provided,
        then it is set to 'No description provided'.
    """

    def __init__(self, func, **kwargs):
        self.name = kwargs.get('name') or func.__name__
        if not isinstance(self.name, str):
            raise InvalidCommandParam(
                str(kwargs.get('name')), 'name', 'string', type(kwargs.get('name')))
        self.callback = func

        # Set the description of the function to the given kwarg.
        self.description = kwargs.get('description')

        # If the kwarg wasn't given, then default to the docstring. If the
        # docstring isn't set, then default to 'No description provided'.
        if self.description == None:
            try:
                if func.__doc__.expandtabs().split('\n') == None:
                    self.description = 'No description provided.'
                else:

                    # We format the docstring.
                    self.description = ''
                    for word in func.__doc__.expandtabs().split('\n'):
                        self.description += word + ' '
            except AttributeError:
                self.description = 'No description provided.'
