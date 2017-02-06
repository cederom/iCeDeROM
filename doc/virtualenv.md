# Python Virtual Environment Reference Manual

This short document presents virtualenv setup guide for iCeDeROM project.

In short words **Virtualenv** is a dedicated and independent **container**
for **Python Application** along with its **Dependencies**.
Different Operating Systems may be bundled with different versions of
Python and different set of available packages by default.
This makes project **deployment** and **maintenance** difficult,
if possible at all.
This is why we want to create from scratch dedicated environment
that we can control.
**Virtualenv** is here to make it happen in an **automated** way.


## Using Virtualenv

iCeDeROM project contains several scripts that will make it easier
for you develop, test, and deploy it using provided Virtualenv.
Assuming that you already did a successful setup of Virtualenv:

* `venv.sh` script will take you inside `bash` shell with target python
environment in path, so you can test some code.
* `iCeDeROM.sh` script will launch the application using virtualenv.


## Creating Virtualenv

* We are using the `Python 3.6` interpreter and so `python3.6 -m venv`.
* You can get Python [directly
from the Python Project Website]
(https://www.python.org/downloads/) or using your
Operating System Package Management.
* iCeDeROM assumes virtualenv location at `../venv/default/` from the
project root (that is where `venv.sh` is located). This location is important!
* If you work with [PyCharm IDE](https://www.jetbrains.com/pycharm/) go to `Preferences / Project / Interpreter`
and use creator to make all work for you.
* You can create Virtualenv from a Terminal (`copies` will copy the
files instead of creating symlinks, `clear` will clear the target directory
if existed previously):
```
$ mkdir ../venv
$ python3.6 -m venv --copies --clear ../venv/macos-python-3.6
$ ln -s macos-python-3.6 ../venv/default
```

* You can have multiple instances of virtualenv in `../venv` directory,
for instance when you develop on [MacOS](https://en.wikipedia.org/wiki/MacOS)
and deploy on [FreeBSD](https://en.wikipedia.org/wiki/FreeBSD),
just remember to link the one you need as `default`.
* Virtualenv shell requires `bash` to run.
* You can test your setup with:
```
$ pwd
/(...)/iCeDeROM/iCeDeROM.git
$ ./venv.sh
(macos-python-3.6) pwd
/(...)/iCeDeROM/iCeDeROM.git
(macos-python-3.6) which python
/(...)/iCeDeROM/venv/macos-python-3.6/bin/python
(macos-python-3.6) python
Python 3.6.0 (default, Dec 23 2016, 12:50:55)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.38)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## Installing dependencies

After you have installed the virtualenv you need to install project
dependencies, that is libraries and modules that the project depends on.
Here is an example:

```
$ ./venv.sh
(macos-python-3.6) pip install -r requirements.txt
...
```

<hr/>
<sup>(C) 2017 [CeDeROM Tomasz CEDRO](http://www.tomek.cedro.info), All rights reserved! :-)</sup>
