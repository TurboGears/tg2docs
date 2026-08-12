TurboGears documentation source
===============================

This repository contains the Sphinx source for the TurboGears 2.5 development
documentation. Framework and extension dependencies follow the development
branches listed in ``requirements.txt``, so builds reflect current source and
can change over time.

Build locally with Python 3.12, the version used by Read the Docs::

    python3.12 -m venv .venv
    . .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    python -m sphinx -W --keep-going -b html docs docs/_build/html

The rendered documentation is in ``docs/_build/html``. Before opening a pull
request, also check external links::

    python -m sphinx -W --keep-going -b linkcheck docs docs/_build/linkcheck

Contributing
------------

Keep changes focused, preserve existing reStructuredText style, and include the
build command and result in the pull request. Report documentation problems at
https://github.com/TurboGears/tg2docs/issues.

