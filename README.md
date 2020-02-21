# **Thank you for using CustConsole.**

## **A customizable console (CLI) created by Jordan Chesley.**

[![CustConsole Version](https://img.shields.io/pypi/v/custconsole?label=version)](https://pypi.org/project/custconsole/) [![Release](https://img.shields.io/badge/release-experimental-orange)](https://pypi.org/project/custconsole/) [![Python Version](https://img.shields.io/pypi/pyversions/custconsole)](https://www.python.org) [![Documentation Status](https://readthedocs.org/projects/custconsole/badge/?version=latest)](https://custconsole.readthedocs.io/en/latest/?badge=latest)

CustConsole is a Python module that helps programmers design a customizable console(s) without having to go through the hassle of defining several methods. The main feature of CustConsole is that programmers can define their own custom commands for the console, in which users can call straight from the command line. CustConsole can automatically parse the console input and execute the user-defined methods with an unlimited number of arguments and keyword arguments.

You can find [CustConsole's documentation here](https://custconsole.readthedocs.io/en/latest/index.html).

You can also [visit the repository here](https://github.com/JordanChesley/custconsole).

To get started with CustConsole, let's build a starter file together!

#### **Setup**
Let's create a new Python file. For this example, we'll call it `console.py`.

Now, inside `console.py`, import the `custconsole` package:


```python
import custconsole
```

#### **Creating an instance of the console**
When creating an instance of the console, we can input a couple of parameters.

- We can give our console a name (Defaulted to "Custom Console")

- We can assign a version number to our console (Defaulted to "0.1")

- We can input a console author (Defaulted to **None**)

Let's create an instance of the console. We will save this instance in the "cc" variable. We will call our console "Test Console", have the version set to "0.0.1", and we can set the author as our name (for mine, I'll write "Jordan Chesley").

```python
cc = custconsole.custconsole(name='Test Console', version='0.0.1', author='Jordan Chesley')
```

#### **Defining a custom command**
Let's create some custom commands.. We use the `@custconsole.command()` decorator above a function to define a custom command. This decorator can take a couple of parameters:

- We can pass a command name (Defaults to the function name)

- We can also pass a command description (Defaults to the function's docstring. If not provided, it then defaults to "No description provided.")

Let's create a command named "hello" which takes no parameters, and will simply print "Hello World!" to the console. Using our existing console instance, we define our command below:

```python
@cc.command()
def hello():
  """Prints 'Hello World!'"""
  print('Hello World!')
```

That was overly simple! Now let's create another command, "echo", which will take an infinite number of arguments, combined to make one string literal, and print it out to the console. We will pass a `description` parameter to the decorator instead of providing a docstring.

```python
@cc.command(description='Return the given input to the console.')
def echo(*sentence):
  print(*sentence)
```

Done! So far, this is our `console.py` file:

```python
import custconsole

cc = custconsole.custconsole(name='Test Console', version='0.0.1', author='Jordan Chesley')

@cc.command()
def hello():
  """Prints 'Hello World!'"""
  print('Hello World!')

@cc.command(description='Return the given input to the console.')
def echo(*sentence):
  print(*sentence)
```

#### **Creating a run script**
CustConsole's goal is to provide a customizable console for its users. Therefore, custconsole doesn't come predefined with a run method. With this in mind, our current file is essentially useless unless we make our own run process. So, let's create one!

For this example, we'd like to print our console header to the console. This header includes our console name, version, and the author name. Continuing in `console.py`, after all of our defined commands:

```py
print(cc.header)
```

Now, let's make a way for users to input the command and arguments. We would like them to be able to type as many commands as they want, so we should loop this with a `while` statement. We can create a custom prompt for them like so:

```py
while True:
  command = input('\nconsole>> ')
```

After, we want to be able to invoke (execute) the command to perform one of our custom commands. CustConsole provides a command parser that can invoke a command and pass any given arguments into it. We use `custconsole.invoke_command()` and pass in our console input to do this:

```py
while True:
  command = input('\nconsole>> ')
  cc.invoke_command(command)
```

In technicality, we've actually finished building a minimal and functioning run script. If you properly enter defined commands without flaw, everything will work just fine. This is our full `console.py` script:

```python
import custconsole

cc = custconsole.custconsole(name='Test Console', version='0.0.1', author='Jordan Chesley')

@cc.command()
def hello():
  """Prints 'Hello World!'"""
  print('Hello World!')

@cc.command(description='Return the given input to the console.')
def echo(*sentence):
  print(*sentence)

print(cc.header)
while True:
  command = input('\nconsole>> ')
  cc.invoke_command(command)
```

If we currently ran this script, the following would be our output:

```
Test Console v[0.0.1] created by Jordan Chesley.
Type 'help' for a list of commands.

console>> help
hello        Prints 'Hello World!'
echo         Return the given input to the console.

console>> hello
Hello World!

console>> echo I love custconsole!
I love custconsole!

console>>
```

#### **Upgrading our run script**

So what if we tried calling a command that didn't exist? Let's try calling a non-existent command named "print":

```
Test Console v[0.0.1] created by Jordan Chesley.
Type 'help' for a list of commands.

console>> print
Traceback (most recent call last):
 File "c:/Projects/test.py", line 17, in <module>
  cc.invoke_command(command)
 File "c:\Projects\custconsole\custconsole.py", line 361, in invoke_command
  raise UnknownCommandError(command)
UnknownCommandError: 'print' is not a command. Type 'help' for a list of commands.
```

To our interest, an exception was raised. If this is unhandled, then users will experience a console that constantly crashes after invoking false commands. We can use a `try/except` statement to handle this error. Return to the run script in `console.py` and add this around the `custconsole.invoke_command()` method:

```python
while True:
  command = input('\nconsole>> ')
  try:
​    cc.invoke_command(command)
  except custconsole.UnknownCommandError as e:
​    print(e)
```

Now when we type a false command into the console, we result this instead:

```
Test Console v[0.0.1] created by Jordan Chesley.
Type 'help' for a list of commands.

console>> print
'print' is not a command. Type 'help' for a list of commands.

console>>
```

Our console instance continues to run, yet handles the error and informs the user instead of crashing the program.

#### **Login to the console**
CustConsole comes with ability to have users register and login to the console. Their console logins are encrypted with a randomly-generated key. In order to perform this though, the programmer must create a "users" file in the same directory as the console script. We have a couple of methods at our hands:

- `custconsole.current_user` is the user account currently logged into the console. If there is no user logged in, this is set to **None**.

- `custconsole.register_user()` allows us to manually register a user login to the console. You can pass optional parameters: a username, and a password.

- `custconsole.login()` prompts the user to login with the proper credentials. If this is called and no user is registered, then this will automatically call **custconsole.register_user()**.

- `custconsole.auth_user()` checks to see if the user's owner is the one initiating the command. They will be asked to verify their password. This returns a boolean statement.

For our example, we'd like the user to login to the console once the console starts up. We'll add the following to our `console.py` script:

```python
while True:
## ADD LOGIN CODE ##
  # The following line is a precautionary to make sure the
  # user HAS to be logged in to use the console.
  if cc.current_user is None:
​    cc.login()
## END ADDED CODE ##
  command = input('\nconsole>> ')
  try:
​    cc.invoke_command(command)
  except custconsole.UnknownCommandError as e:
​    print(e)
```

Now if we run our updated script, we should get the following:

```
Test Console v[0.0.1] created by Jordan Chesley.
Type 'help' for a list of commands.

No user is registered. Please create a user below.

Username:
```

We can go ahead and create an account. For this tutorial, I'll make an account with the username of "guest" and a password of "guest".

```
Username: guest
Password: 
Verify password for new user guest: 
Registered guest.

Username:
```

Now we can log in with our credentials>

```
Username: guest
Password: 
Logged in as guest.

console>>
```

Excellent. This is our full `console.py` file now:

```python
import custconsole

cc = custconsole.custconsole(name='Test Console', version='0.0.1', author='Jordan Chesley')

@cc.command()
def hello():
 """Prints 'Hello World!'"""
 print('Hello World!')

@cc.command(description='Return the given input to the console.')
def echo(*sentence):
 print(*sentence)

print(cc.header)
while True:
 if cc.current_user is None:
  cc.login()
 
 command = input('\nconsole>> ')
 try:
  cc.invoke_command(command)
 except custconsole.UnknownCommandError as e:
  print(e)
```

Congratulation! You've made your very own custom console! Now, you can go and make your own consoles to use for your own applications. Take a look at the documentation [](here) to look at methods not covered by this tutorial.
