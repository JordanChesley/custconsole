"""
The base of the console containing the necessary methods
to run the custom console.
"""

__all__ = ['Commands', 'custconsole', 'Help']

import binascii
import datetime
from getpass import getpass
import os
import random
import time

from .errors import InvalidCommandParam, UnknownCommandError, DuplicateCommandError, BadLogoutCall, ArgumentError

class custconsole():
  """
  Creates an instance of the custom console.
     
  Parameters
  ----------
  name: Optional[:class:`str`]
      The name of the console. This is defaulted to 'Custom
      Console'.
     
  author: Optional[:class:`str`]
      The name of the author writing the console e.g. your
      name or nickname. This is defaulted to NoneType.
     
  version: Optional[:class:`str`]
      The version number of your console. This number should
      be regularly updated in relevance to the amount of
      updates you've implemented. This is defaulted to '0.1'.
  """

  def __init__(self, **attrs):
    self.name = attrs.get('name') if 'name' in attrs else 'Custom Console'
    self.author = attrs.get('author') if 'author' in attrs else None
    self.version = attrs.get('version') if 'version' in attrs else '0.1'

    # Let's format the console header. Always include the following line:
    self.header = f'{self.name} v[{self.version}]'

    # The author may not be given. If they are, let's include them in
    # the header.
    if self.author != None:
      self.header += f' created by {self.author}.'
    
    # Always include and finish with this statement:
    self.header += '\nType \'help\' for a list of commands.'

    self.current_user = None

    # We ensure the existance of a 'users' file
    f = open('users', 'a')
    f.close()

    self.commands = {}
    self.visible_commands = {}
  
  def auth_user(self, username=None, pwd=None):
    """
    Checks to make sure the user enters the right credentials
    during login before giving access to the account.
       
    Parameters
    ----------
    username: Optional[:class:`str`]
        The username of the account to verify.

    pwd: Optional[:class:`str`]
        The user's login password. This should normally be
        left blank so that the user verifies their password.

    Returns
    -------
    :class:`bool`
        Returns 'True' if the user's input matches their
        credentials and therefore are authorized.

        Returns 'False' if the user's input doesn't match
        their credentials and therefore aren't authorized.
    """

    # If we receive the default parameter values, let's have the
    # username set to the logged in user's name. Then we ask the
    # user to enter their account password.
    if username == None:
      username = self.current_user
    if pwd == None:
      pwd = getpass()
    
    __users = {}
    lncount = 0

    # We grab their account information from a bytes file.
    with open('users', 'rb') as f:
      cntnt = f.readlines()
    for line in cntnt:
      lncount += 1

    # Organize the bytes into a readable format.
    for i in range(int(lncount)):
      line = cntnt[i].strip(b'\n').split(b': ')
      name = str(line[0]).replace('b\'', '').replace('\'', '')
      encPwd = bytes(line[1])
      encPwd = encPwd.replace(b'b\'', b'').replace(b'\'', b'')
      __users[name] = encPwd

    # Here starts the actual authorization process.
    for __user in __users:
      if __user == username:
        if self.decrypt(bytes(__users[username])) == pwd:
          return True
    return False

  def register_user(self, username=None, pwd=None):
    """
    Register an account to login to the console.
            
    This is automatically called by the console when there's
    no available users to login to the console. This can also
    be manually called by the user.

    Parameters
    ----------
    username: Optional[:class:`str`]
        The username wished to be registered.
          
    pwd: Optional[:class:`str`]
        The password wished to be used to login to the user.
    """

    print('')
    # If the user called this function without parameters, we want
    # the user to input the parameters.
    if username == None:
      username = input('Username: ')

    # We ensure that the user enters a valid username.
    while username.isspace():
      username = input('Enter a valid username: ')
    
    # We also ensure that the user being registered doesn't already exist
    # in the user list.
    lncount = 0
    users = []

    with open('users', 'rb') as f:
      cntnt = f.readlines()
    for line in cntnt:
      lncount += 1
      
    for i in range(int(lncount)):
      line = cntnt[i].decode('utf-8')
      line = line.strip('\n').split(': ')
      users.append(line[0])
      i += 1

    if username in users:
      print('User already exists. Please use a different username.')
      return self.register_user()
    
    # We ensure the user enters a valid password.
    if pwd == None:
      pwd = getpass()
    while pwd.isspace():
      pwd = getpass('Enter a valid password: ')

    # Always verify the chosen password in any scenario. If the passwords
    # match, continue. Else, rerun the function and pass the entered
    # parameters and just ask to verify the password again.
    vp = getpass(f'Verify password for new user {username}: ')
    if pwd == vp:
      encPwd = self.encrypt(pwd)

      # Insert information onto one line.
      line = f'{username}: {encPwd}\n'.encode('utf-8')
      with open('users', 'ab') as f:
        f.write(line)
      self.spin(f'Registering {username}...', 3)
      print(f'Registered {username}.')
    else:
      self.register_user(username, pwd)

  def login(self, username=None, pwd=None, auto_reg=True):
    """
    Prompt a user to login to the console.
       
    If no user exists in the console, then this function
    automatically calls the :meth:`custconsole.register_user()`
    function.

    The console programmer may also want to automatically login
    a user when the console runs. They may optionally pass the
    username and password as kwargs to automatically login the
    user.

    Parameters
    ----------
    username: Optional[:class:`str`]
        The username of the account to login with.
    
    pwd: Optional[:class:`str`]
        The password of the account to login with.
    
    auto_reg: Optional[:class:`bool`]
        Toggles auto-registration if the console has no
        registered user in it. This is automatically set
        to True. If you do NOT want the console to create
        a user, then set this to False.
    """

    loginUsername = username
    loginPwd = pwd
    if auto_reg:
      # Let's first check to see if any users currently exist.
      with open('users', 'rb') as f:
        lines = f.readlines()
      if len(lines) == 0:

        # There's no user registered for this console yet. Let's add
        # one.
        print('\nNo user is registered. Please create a user below.')
        self.register_user()
        print('')
    
    # We then continue to login.
    while True:
      if loginUsername == None:
        loginUsername = input('\nUsername: ')
        loginPwd = getpass()
      if self.auth_user(loginUsername, loginPwd):
        self.current_user = loginUsername
        self.spin('Logging in...', 2)
        print(f'Logged in as {self.current_user}.')
        break
      else:

        # We got here because the user failed to enter the right
        # username or password.
        self.spin('Logging in...', 4)
        print('Incorrect username or password.')
  
  def logout(self, force_auth=False):
    """
    Log out the current console user.
       
    Parameters
    ----------
    force_auth: Optional[:class:`bool`]
        Optional parameter. Force the user to authorize
        themselves to confirm their action. This is
        automatically set to False.
      
    Raises
    ------
    BadLogoutCall
        Raised when this method is called while no one is
        logged into the console. This will attempt to
        force the console to quit.
    """
    if self.current_user == None:
      raise BadLogoutCall
    if force_auth:
      if self.auth_user():
        self.spin(f'Logging out of {self.current_user}...', 3)
        print(f'Logged out of {self.current_user}.')
        self.current_user = None
      else:
        print(f'{self.current_user} is not authorized. Logout failed.')
    else:
      self.spin(f'Logging out of {self.current_user}...', 3)
      print(f'Logged out of {self.current_user}.')
      self.current_user = None


  def spin(self, text, spins):
    """
    Create a fancy looking spinner for your console.
       
    Parameters
    ----------
    text: :class:`str`
        This is the text that you want to display next to
        the spinner. This function will automatically
        place a ' ' space next to the text.
       
    spins: :class:`int`
        The amount of times you want the spinner to spin.
        To help determine the number of spins, the spinner
        spins a full rotation in 0.4 seconds.
    """
    animation = ["/", "-", "\\", "|"]
    end = ""
    for _ in range(spins):
      for char in animation:
        print("\r" + text + " " + char, end="")
        time.sleep(0.1)
    for char in text:
      end += " "
    print("\r  ", end=end + "\r")

  def encrypt(self, target):
    """
    Encrypt an object.

    Parameters
    ----------
    target: :class:`str`
        The object that is being encrypted.
       
    Returns
    -------
    :class:`bytes`
        Encrypted object.
    """

    # Convert target to B64 bytes.
    conv = binascii.b2a_base64(target.encode(), newline=False)

    # If necessary, we translate to a simpler format.
    conv = conv.translate(bytes.maketrans(b'+/', b'-_'))

    # Generate throwoff bytes.
    _key = ''
    alphanumeric = 'abcdefghijklmnopqrstuvwxyz0123456789'
    for _ in range(len(target)):
      place = random.randint(0, 35)
      _key += alphanumeric[place:place+1]
    _key = binascii.b2a_base64(_key.encode(), newline=False)
    _key = _key.translate(bytes.maketrans(b'+/', b'-_'))

    # Implement throwoff into encryption.
    enc = b''
    for i in range(len(conv)):
      enc += conv[i:i+1] + _key[i:i+1]

    return enc
  
  def decrypt(self, target):
    """
    Decrypt an object with the key used to encrypt it.

    Parameters
    ----------
    target: :class:`bytes`
        The object that is being decrypted.
    
    Returns
    -------
    :class:`str`
        Decrypted object.
    """

    # Grab the real encrypted target.
    real = b''
    for i in range(len(target)):
      if i % 2 == 0:
        real += target[i:i+1]

    # If necessary, transalate to B64 format.
    real = real.translate(bytes.maketrans(b'-_', b'+/'))

    # Translate in ASCII bytes. Then stringify it.
    dyc = str(binascii.a2b_base64(real)).replace('b\'', '').replace('\'','')

    return dyc
  
  def help(self):
    """
    Print a list of commands to the console.
       
    These commands are listed by name and description. The
    name is either the name of the function or the value of
    the 'name' kwarg (if set). The description is either the
    function's docstring or the 'description' kwarg (if set).
    It is recommended that a 'description' kwarg is set up.
    """
    # Run the __init__ of the Help class, passing the command
    # dictionary.
    Help(self.visible_commands)

  def _add_command(self, command, hidden):
    """
    Adds a command to the console's command list.
    This should never be called manually.
       
    Parameters
    ----------
    command: :class:`.Commands`
        The command that's being added. Must be formatted
        with the 'Commands' class. 
       
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
    self._alphabetize_commands(self.commands, 1)
    self._alphabetize_commands(self.visible_commands, 2)


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

  def _alphabetize_commands(self, command_list, list_id):
    """
    We use this function to list our commands in alphabetical
    order. This should never be called manually.

    Parameters
    ----------
    command_list: :class:`dict`
        This is the command list holding the custom commands.
        This is normally custconsole.commands.
       
   list_id: :class:`int`
        Tells what list to manipulate:
          1 = self.commands
          2 = self.visible_commands
    """

    ordered_list = {}
    i = 0
    keys = sorted(command_list)
    for _ in range(len(command_list)):
      ordered_list[keys[i]] = command_list[keys[i]]
      i += 1
    if list_id == 1:
      self.commands = ordered_list
    elif list_id == 2:
      self.visible_commands = ordered_list

  def _parse_command(self, command_string):
    """
    Parse the given command into the command name, arguments,
    and keyword arguments. This function is called by the
    :meth:`custconsole.invoke_command()` function and should not be
    called manually.

    Parameters
    ----------
    command_string: :class:`str`
        This is the string passed into custconsole.invoke_command().
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
    """

    # Separate the command and the parameters.
    cmd, pars = command_string.split(' ', maxsplit=1)
    args = []
    kwargs = {}
    detecting_keyword = False

    # Adding a space at the end helps us better parse the params.
    pars += ' '

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
        elif char == '\'':
          start = pars.find(char)
          end = pars[start+1:].find(char) + 2
          if detecting_keyword:
            kwargs[variable_name] = pars[start:end]
            detecting_keyword = False
          else:
            args.append(pars[start:end])
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
              detecting_keyword = False
            else:
              args.append(pars[:end])
          pars = pars.replace(pars[:end + 1], '', 1)
          break
    return cmd, args, kwargs
    

  
  def invoke_command(self, command_string):
    """
    Executes the given command. This is usually the console user's
    input.
       
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
        Raised when too many or too little arguments are given.
    """

    # custconsole._parse_command() returns 3 objects so we assign
    # three variables to the method.
    if len(command_string.split()) > 1:
      command, args, kwargs = self._parse_command(command_string)
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

  def command(self, name=None, hidden=False, *args, **kwargs):
    """
    A decorator used to define custom commands for your console.

    Parameters
    ----------
    name: Optional[:class:`str`]
        Name of the command. This is defaulted to the function name.
       
    description: Optional[:class:`str`]
        Command's description. This will default to the function's
        docstring. If a docstring is not provided, it will then
        default to 'No description provided.'
       
    hidden: Optional[:class:`bool`]
        Controls if the command is shown in the (default) help
        command. If False, this will place the command in a
        custconsole.visible_commands dictionary, as well as place
        it in the custconsole.commands dictionary, which shows all
        commands. This is defaulted to False.
    
    Example
    -------
    .. code-block:: python

        cc = custconsole.custconsole()

        @cc.command(description='Echos given statement.', hidden=True)
        def echo(*phrase):
          print(*phrase)
        
        @cc.command()
        def logout():
          cc.logout()
    
    """

    def decorate(func):
      result = Commands(func, name=name, *args, **kwargs)
      self._add_command(result, hidden)
      return result

    return decorate
  
class Commands():
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
      raise InvalidCommandParam(str(kwargs.get('name')), 'name', 'string', type(kwargs.get('name')))
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

class Help():

  # In technicality we could just have the following code
  # executed in the custconsole.help() function. We do this
  # simply to help find this portion of code faster.
  def __init__(self, commands):
    for command in commands:
      command = commands[command]
      name = command.name.ljust(20)
      desc = command.description
      print(name, desc)
