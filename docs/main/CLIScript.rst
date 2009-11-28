.. _cli_script:

Command Line Scripts
####################

It is often useful to have command line scripts that can access the
model of a TurboGears2 application, as an example, to manipulat model
object from within a cron job.  The main difficulty in implementing
such a script is often to have the model configured according to a
given configuration file.  Paste takes care of that but the
documentation of it's API can seem somewhat obscure to newcomers.

Example Command Line Script
===========================

The following script prints all the usernames to the console.  The
critical part of the script is the `load_config()` function.  It both
parses the `.ini` configuration file and initializes the SQLAlchemy
model.

.. code-block:: python

    #!/usr/bin/env python
    """ Print all the usernames to the console. """
    import os
    import sys
    from argparse import ArgumentParser

    from paste.deploy import appconfig
    from example_app.config.environment import load_environment
    from example_app import model

    def load_config(filename):
        conf = appconfig('config:' + os.path.abspath(filename))
        load_environment(conf.global_conf, conf.local_conf)

    def parse_args():
        parser = ArgumentParser(description=__doc__)
        parser.add_argument("conf_file", help="configuration to use")
        return parser.parse_args()

    def main():
        args = parse_args()
        load_config(args.conf_file)

        print model.DBSession.query(model.User.user_name).all()

    if __name__ == '__main__':
        sys.exit(main())


Packaging and Deploying CLI Scripts
===================================

Setuptools can take care of installing CLI script in the `$PATH` when
an application is installed or set it ``development`` mode.  For this
to happen, all what one have to do is to include a reference to his
scripts in the `console_scripts` entry point in `setup.py`.  As an
example, if the above script is saved in saved as
`exampleapp/scripts/usernames.py`, then `setup.py` should contain the
following:

.. code-block:: python

    setup(#...
     entry_points="""
     # ...
     [console_scripts]
     print-usernames = exampleapp.scripts.usernames:main
     """)
