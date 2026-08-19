======================================
Preparing Your Development Environment
======================================

Install Git
===========

Install a current version of `Git`_. The `Git documentation`_ contains
installation and usage guidance.

Create a Python environment
===========================

TurboGears development uses Python 3.10 or newer. Create and activate an
isolated virtual environment before installing the projects::

    $ python3 -m venv .venv
    $ . .venv/bin/activate
    $ python -m pip install --upgrade pip

Clone the repositories
======================

The main repositories are:

`TG2 Core`_
    The TurboGears framework.

`TG2 Devtools`_
    The Gearbox-based development tools and application templates.

`TG2 Docs`_
    This documentation project.

Clone the repositories and use their current ``development`` branches::

    $ git clone https://github.com/TurboGears/tg2.git
    $ git clone https://github.com/TurboGears/tg2devtools.git
    $ git clone https://github.com/TurboGears/tg2docs.git
    $ cd tg2
    $ git switch development
    $ cd ../tg2devtools
    $ git switch development
    $ cd ../tg2docs
    $ git switch development

Install the projects
====================

Install the documentation dependencies first. The requirements file includes
TurboGears development checkouts, so install the local editable projects again
afterward to ensure that local changes are the versions being used::

    $ cd ../tg2docs
    $ python -m pip install -r requirements.txt

Install the framework and development tools from their working trees in
editable mode. The ``testing`` extra installs their test dependencies::

    $ cd ../tg2
    $ python -m pip install -e ".[testing]"
    $ cd ../tg2devtools
    $ python -m pip install -e ".[testing]"

Changes in those working trees are now available immediately to the
environment. For a focused contribution, work in the repository that owns the
change and add or update its tests.

Repository links
================

.. _Git: https://git-scm.com/
.. _Git documentation: https://git-scm.com/docs
.. _TG2 Core: https://github.com/TurboGears/tg2
.. _TG2 Devtools: https://github.com/TurboGears/tg2devtools
.. _TG2 Docs: https://github.com/TurboGears/tg2docs
.. _Gearbox: https://github.com/TurboGears/gearbox
.. _tickets: https://github.com/TurboGears/tg2/issues
