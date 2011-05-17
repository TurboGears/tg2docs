.. _command_line_reference:

Command Line Reference
######################


TurboGears2 delegates its command line tasks to Paste.  TG1.x uses the
built-in command ``tgadmin`` which was dropped in favor of the more
robust Paste infrastructure.

What is PasteScript?
====================

PasteScript is a part of the Paste group of libraries, which provides
the very basic foundation on which TurboGears and Pylons are
built. You can think of Paste_ as a very useful group of things.

.. _Paste: http://pythonpaste.org/

As for PasteScript_ it is composed of two parts Templates and Commands,
the first takes care of code generation tasks (like quickstart), the
second is an extensible command line utility (like tginfo)

.. _PasteScript: http://pythonpaste.org/script/

If you are interested in learning how to build your own Paster command
please visit http://pythonpaste.org/script/developer.html

How Does It Integrate With TurboGears 2?
========================================

PasteScript provides a single command-line script named ``paster``
which is built to be self-explanatory.  Try it out on the command
line: it should give you a big list of commands. There is also a
``paster help <command>`` command that will give you additional
information about all commands that it provides.

Using a setuptools mechanism known as "entry point" TurboGears, as
well as any other project that uses PasteScript, is able to add
extensions to the paster command; for example if you execute paster
with no parameters you will see a "TurboGears2" section.

.. _commandline-reference:

What are the TurboGears commands?
==================================

Please note that not all ``paster`` commands are expected to work with
a TurboGears |version| project. However, if you experience an error using
paster we encourage you to report it. Below is a list of the most important
commands you will use in your journey in the world of TurboGears |version|.
Be sure to run ``paster help`` on each of them to get all the possible command
line switches.

====================================  ===========================================
paster command                        action
====================================  ===========================================
`paster quickstart`_ <project_name>   initialize new project
`paster serve`_  <config_file>        serve project configured in <config_file>
`paster tginfo`_                      list tg files in current path
`paster shell`_ <config_file>         start python shell, loading project models
`paster setup-app`_  <config_file>    initialize project using config_file
====================================  ===========================================


.. _paster quickstart:

paster quickstart
------------------

This is probably the first command you will encounter when developing
on TurboGears, it will create a base project for you with everything
you need to get started and explanations for everything. In case you
are wondering this is a small wrapper around ``paster create`` to
provide a TG1-like command.

.. _paster serve:

paster serve
------------

This is used to start the built-in server.  This is a very robust
implementation (multi-threaded, SSL support, etc.) which means several
people use it in production. That said, you should take a look at our
:ref:`tgdeployment` docs. The most common usage for this command is:

.. code-block:: bash

     $ paster serve --reload development.ini

The above command will enable the reloading of the server every time
you save a file, which is a very nice feature :)

.. _paster tginfo:

paster tginfo
--------------

This command is designed to display a rather big chunk of information
regarding your TurboGears installation, and it's designed to
troubleshoot installation problems. Therefore it should be the first
thing you should run to be certain your system is healthy.

.. _paster shell:

paster shell
-------------

This starts a python shell with your TurboGears application
loaded. The most important feature here is that your model is also
loaded, therefore you can experiment with your database.

.. note::

    Changes made to your database from within `paster shell` are
    encapsulated in a transaction.  In other words, your changes won't
    be saved unless you commit::

        import transaction
	transaction.commit()

.. _paster setup-app:

paster setup-app
----------------

setup-app provides two crucial pieces of functionality.

1) Set up your database schema.
2) Add bootstrap data to your database.

Your project will have a folder called websetup which contains
schema.py and bootstrap.py. Each of these can be customized to add
additional functionality to your bootstrapping process.  For instance,
if you have additional default users you would like added, you would
add them in at the bottom of bootstrap.py inside the bootstrap()
function, before the transaction.commit().  The command looks
something like this::

     paster setup-app development.ini
