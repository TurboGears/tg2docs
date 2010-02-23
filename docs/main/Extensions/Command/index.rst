.. _tgext.command:

TGExt.Command
=============

TurboGears uses the Paste commands system to create command-line entry
points that, for example, set up your database or start your server.
When you get to larger projects, however, you will often have other
things you need to do "in the context of your application" from the
command line, such as periodic imports of data, or cron'd database
management tasks.

Paste's command system is well documented, but it can take quite a bit
of poking around to find out how to get SQLAlchemy, and TurboGears
configured so that code that looks in tg.config gets the right values,
and SQLAlchemy has access to your models.

This extension (tgext.command) is an attempt to make it
easier to create new TG command-line commands.

.. code-block:: bash

    $ easy_install tgext.command

To use the extension, you will create a BaseCommand class like this
that will be shared by all of your command-line scripts.

.. code-block:: python

    from tgext.command import tgcommand
    class BaseCommand( tgcommand.TGCommand ):
        def import_model( self ):
            from example import model
            return model

This command-class would then serve as the base command for each of
your "real" commands.  For example, a command that iterates through
all users showing their user_name property:

.. code-block:: python

    class Hello(BaseCommand):
        def db_command( self, engine ):
            from example.model import User,Group, DBSession
            for user in DBSession.query( User ):
                print 'User',user.user_name

As with regular Paste commands you have to register your TGCommands
in your application's setup.py (in the setup() call), like so:

.. code-block:: ini

    entry_points="""
    [paste.paster_command]
    hellocommand = example.commands.hello:Hello
    """

You will need to re-run setup.py develop to get the command to be
available).  Note that a simple approach which does not support
PID-file exclusion, paster registration/command-line-parsing and
the like is documented in :ref:`cli_script`.
