.. _tg-starting:

=========================
TurboGears2 Documentation
=========================

This section covers documentation about getting started with TurboGears2.

For a fresh TurboGears 2.5 quickstart, create the project, install the generated
package into your active environment, initialize it, and then serve it::

    gearbox quickstart myproject
    cd myproject
    python -m pip install -e .
    gearbox setup-app -c development.ini
    gearbox serve -c development.ini --reload

Use ``python -m pip install -e '.[testing]'`` if you also want to run the
generated tests. Current quickstarts generate ``development.ini`` and
``test.ini``; production configuration is something you add for your deployment.

The following chapters cover the most common features of TurboGears, introductions
to them and some intermediate features.

.. toctree::
    :maxdepth: 2

    controllers
    templating
    kajiki-xml-templates
    scaffolding
    validation
    webflash
    widgets_forms
    authorization
    pagination
    session
    caching
    i18n
    profiling
    api
    agent-tooling
    Pluggable/index
    restdispatch
    migrations
    gearbox
    mongodb
    objectdispatch
    testing
    configuration/index
    authentication
    hooks
