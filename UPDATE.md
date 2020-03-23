# Welcome to the CustConsole 0.1 Update!

###### I've been trying get this update out faster but was having trouble uploading to PyPI.

Welcome to what I consider the official beta. I know there has been trouble for most when installing the package. I'm working to resolve the installation error by minimizing the number of other packages used to help make this work. This is my first time creating a package; please bear with me.



In any case, what you want is the update information. Here's what new and/or modified:

* **Encryption / Decryption Remake**
* **Added automatic login feature for *custconsole.login()***
* All documentation ahs been updated. Remember [you can find the documentation at ReadTheDocs](https://custconsole.readthedocs.io/en/latest/index.html).



I like to call this update the ***Cryptography Update***.



## Encryption / Decryption Remake

The *custconsole.encrypt()* and *custconsole.decrypt()* methods have been completely remodeled. The methods originally relied on a package called "cryptography", which the user had to install onto their system (done automatically when installing custconsole). I've removed this package and stuck to the pre-installed packages that come with Python 3 in hopes that it would resolve the "Microsoft Visual C++ 14.0 is required" error.



> **def encrypt(self, target)**
>
> Encrypt an object.
>
> #### Parameters
>
> target: :class:`str`
>
> ​    The object that is being encrypted.  
>
> #### Returns
>
> :class:`bytes`
>
> ​    Encrypted object.



> **def decrypt(self, target)**
>
> Decrypt an object with the key used to encrypt it.
>
> #### Parameters
>
> target: :class:`bytes`
>
> ​    The object that is being decrypted.  
>
> #### Returns
>
> :class:`str`
>
> ​    Decrypted object.  



## Automatic login with *custconsole.login()*

"What if the user want to automatically log in to the console?" After debating myself for WHY someone would do it, I decided to just do for those who may want to. All the user has to do is write their username and password inside the method.

> def login(self, username=None, pwd=None, auto_reg=True):
>
>   """
>
>   Prompt a user to login to the console.
>
> If no user exists in the console, then this function automatically calls the :meth:`custconsole.register_user()` function.
>
> The console programmer may also want to automatically login a user when the console runs. They may optionally pass the username and password as kwargs to automatically login the user.
>
> #### Parameters
>
> username: Optional[:class:`str`]
>
> ​    The username of the account to login with.  
>
> pwd: Optional[:class:`str`]
>
> ​    The password of the account to login with.  
>
> auto_reg: Optional[:class:`bool`]
>
> ​    Toggles auto-registration if the console has no  
> ​    registered user in it. This is automatically set  
> ​    to True. If you do NOT want the console to create  
> ​    a user, then set this to False.



#### This concludes my 0.1 update. I hope everything works for everyone and I wish you all happy programming!
