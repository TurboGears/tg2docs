====================
Testing Your Changes
====================

Run the tests before opening a pull request. Use the Python environment and
editable installation described in :doc:`prepenv`.

TurboGears Core and Devtools
============================

From the root of the repository you changed, install its testing dependencies
once::

    $ python -m pip install -e ".[testing]"

Run the complete test suite with pytest::

    $ python -m pytest

TurboGears Core enables ``--cov=tg`` through its pytest configuration, so the
standard command also reports Core coverage. If you need to override the
project configuration, run the coverage option explicitly::

    $ python -m pytest --cov=tg

Documentation
=============

From the ``tg2docs`` repository root, build the HTML documentation with strict
warning handling::

    $ python -m sphinx -W --keep-going -b html docs docs/_build/html

Check external links separately::

    $ python -m sphinx -W --keep-going -b linkcheck docs docs/_build/linkcheck

Fix failures and rerun the relevant command before submitting the change.
