.. _tg-agentic-development:

================================
Agentic TurboGears development
================================

This tutorial shows a small TurboGears 2.5 development session directed by
conversation with a coding agent. The session creates a server-rendered
reading-list page, adds a functional test, and checks the result through
TurboGears project inspection and runtime tools.

The example uses Pi as a **coding-agent harness**: Pi receives prompts, reads
the project, edits files, and runs the requested checks. Pi is not a
TurboGears runtime dependency. The generated application does not import Pi,
and deploying or running the application does not require Pi.

The transcript below records the requests and the agent's intended work. It
does not define Pi command-line syntax. Start the Pi harness according to its
own documentation, then give it the prompts in this page.

What you will build
===================

The finished ``readinglog`` project has a mounted ``/reading`` page. The page
renders a short reading list with these exact titles:

* ``The Left Hand of Darkness``
* ``Kindred``
* ``The Dispossessed``

The page accepts an optional ``topic`` query parameter and renders it as
``Topic: <topic>``. It also has a WebTest functional test for the public HTTP
behavior. The agent uses TurboGears' current project skills rather than
guessing the project layout:

* ``tg-inspect`` uses ``tginfo`` to discover project facts, routes, templates,
  and scaffold templates;
* ``tg-scaffold`` uses ``scaffold`` to create conventional files;
* ``tg-shell`` uses ``tgshell`` for a loaded-application check and
  ``tg.util.webtest.test_context`` when a separately scoped request context is
  needed.

The tutorial intentionally stays within a page, template, and test. It does
not add a model, migration, API, runtime AI feature, or new TurboGears
extension.

Prerequisites
=============

You need:

* Python 3.10 or newer and a working TurboGears 2.5 development environment;
* the ``gearbox`` command and the TurboGears quickstart templates;
* a clean parent directory in which ``readinglog`` does not already exist;
* the Pi coding-agent harness, used only to direct development;
* permission to let the agent read and edit the project files.

Create the project before starting the feature conversation. Run these
commands in the parent directory::

    $ gearbox quickstart readinglog --noauth
    $ cd readinglog
    $ python -m pip install -e '.[development]'
    $ gearbox tgskills

The quickstart creates ``development.ini``, ``test.ini``, project code, tests,
``AGENTS.md``, and the local ``.agents/skills/`` files. The editable install
makes the generated project's Gearbox commands available in the active
Python environment. ``tgskills`` is safe to repeat when the skills need to be
installed for a project; it does not replace an existing skill directory.

This page uses no application setup or database mutation. The feature is a
server-rendered page that can be inspected and tested without initializing a
database. Use ``development.ini`` for project inspection and ``test.ini`` for
isolated test-runtime checks, as shown below.

The prompt transcript
=====================

The prompts are deliberately specific about the product behavior and the
validation boundary. They ask the agent to use the installed skills and the
documented commands, while leaving ordinary Python and template edits to the
agent.

1. Inspect before editing
-------------------------

Give Pi this prompt from the ``readinglog`` project root:

    I am building a reading-list page for this TurboGears 2.5 application.
    Before editing, inspect the project with the tg-inspect skill. Use
    ``gearbox tginfo summary --project . --config development.ini --json``,
    ``gearbox tginfo routes --project . --config development.ini --json``,
    ``gearbox tginfo templates --project . --config development.ini --json``,
    and ``gearbox tginfo scaffolds --project . --config development.ini --json``.
    Report the package name, the root controller source location, the template
    engine, the existing test layout, and the exact scaffold names that can
    create a controller, template, and functional test. Do not edit files yet.

A good response identifies the existing application instead of inventing a
layout. The agent should use the JSON output as project facts and should call
out any import or configuration failure before proposing edits.

Expected inspection evidence includes:

* the generated package and root controller;
* the existing route and template inventories;
* the generated functional-test base class and test directory;
* the available ``controller``, ``template``, and ``controller_test``
  scaffolds.

2. Create one vertical feature slice
------------------------------------

After reviewing the inspection, give Pi this prompt:

    Add the smallest complete reading-list feature. Use the tg-scaffold skill
    and run ``gearbox scaffold controller template controller_test reading``
    from the project root. Mount the generated ReadingController at
    ``/reading`` from the existing RootController. Edit the generated
    controller and Kajiki template so the page displays the heading
    ``Reading list`` and these exact titles: ``The Left Hand of Darkness``,
    ``Kindred``, and ``The Dispossessed``. The action may accept an optional
    ``topic`` query parameter and should render it exactly as ``Topic:
    <topic>`` when supplied. Update the generated functional test to prove
    that ``GET /reading`` returns 200, contains the heading, and contains all
    the three exact titles; add a check for the ``topic`` behavior. Keep the generated
    project conventions and do not change unrelated files. Do not add a model,
    database write, new dependency, or framework code.

The scaffold command creates the conventional starting points. The agent then
edits those generated files directly and mounts the controller; scaffolding
alone does not make a controller reachable. The exact generated class and
module names come from the project package and scaffold output, so the agent
should confirm them rather than copy a guessed import path.

3. Inspect and validate the result
----------------------------------

Give Pi this prompt after it reports the edits:

    Validate the feature from the project root. First use tg-inspect to run
    ``gearbox tginfo routes --project . --config development.ini --json`` and
    ``gearbox tginfo templates --project . --config development.ini --json``;
    confirm that ``/reading`` resolves to the new controller and template.
    Then run ``python -m pytest``.
    Finally use the tg-shell skill with ``gearbox tgshell -c test.ini`` and a
    small temporary script to request ``/reading`` with WebTest, assert status
    200, and check the rendered heading. If a separate fake request scope is
    needed, use ``from tg.util.webtest import test_context`` and
    ``with test_context(app, '/reading')``; do not use an old TurboGears
    request-context API. Report the commands, test result, route, and template
    source locations. Do not mutate the database.

The ``tgshell`` check should be a real request through the loaded WSGI
application, not a direct call to the controller method. A minimal check has
the same shape as the documented skill recipe::

    response = app.get('/reading')
    assert response.status_int == 200
    assert 'Reading list' in response.text

If request-local code must be checked separately, the temporary script can
also use::

    from tg.util.webtest import test_context

    with test_context(app, '/reading'):
        assert request.path == '/reading'

The script is a validation aid, not part of the feature. Remove it after the
agent reports the check, or keep it outside the application package if the
local workflow retains diagnostic scripts.

Expected artifacts
==================

After the feature prompt, the relevant project files should be similar to
this tree (the package name is determined by the quickstart)::

    readinglog/
    ├── AGENTS.md
    ├── development.ini
    ├── test.ini
    ├── .agents/skills/
    │   ├── tg-inspect/SKILL.md
    │   ├── tg-scaffold/SKILL.md
    │   └── tg-shell/SKILL.md
    └── readinglog/
        ├── controllers/root.py
        ├── controllers/reading.py
        ├── templates/reading.xhtml
        └── tests/functional/test_reading.py

The feature-specific files have these responsibilities:

``controllers/reading.py``
    Exposes the reading page and passes the fixed titles and optional topic to
    the template.

``controllers/root.py``
    Mounts ``ReadingController`` so object dispatch reaches ``/reading``.

``templates/reading.xhtml``
    Renders the ``Reading list`` heading, titles, and optional topic using the
    generated Kajiki conventions.

``tests/functional/test_reading.py``
    Exercises the public WebTest response, including the optional topic.

``AGENTS.md`` and ``.agents/skills/`` are generated onboarding artifacts, not
application feature code. Do not commit or modify them as part of this feature
unless the project's own workflow explicitly requires machine-local skill
installation.

Validation checklist
====================

Ask the agent to report each of these signals:

#. ``gearbox tginfo routes --project . --config development.ini --json``
   includes ``/reading`` and its controller source location.
#. ``gearbox tginfo templates --project . --config development.ini --json``
   associates the reading template with ``/reading`` and reports its
   project-relative path.
#. ``python -m pytest`` passes, including the new functional test.
#. The ``tgshell`` WebTest request returns HTTP 200 and contains the rendered
   heading.
#. A request with ``topic`` renders ``Topic: <topic>`` without changing the
   route or template contract.
#. No database write, dependency addition, or unrelated file change was made.

Use ``tginfo`` for facts about application structure and ``tgshell`` for
runtime behavior. ``tginfo`` loads application code even though it is
read-only, so project-defined import and startup side effects can still run.
Treat a nonzero command result as a failed validation and read the reported
stderr before continuing.

Recovery
========

**The quickstart reports a conflict.** A quickstart conflict returns a nonzero
status and identifies the existing name or directory. Stop and choose a new
project name, or inspect the existing project deliberately. Do not ask the
agent to overwrite an unrelated project.

**Project commands are unavailable.** Return to the project root and repeat
the documented editable install. The generated project contributes commands
only after its package and development dependencies are installed in the
active environment.

**Skills are missing.** Run ``gearbox tgskills`` from the project root. If a
skill directory already exists, do not replace it blindly; inspect the local
skill and the installed devtools version, then let the agent use the available
skill instructions.

**Inspection fails.** Confirm that the command runs from the project root and
that the selected config is ``development.ini``. Keep JSON stdout separate
from diagnostics on stderr. An import or startup failure is a project failure
to diagnose, not a reason to infer routes from memory.

**The scaffold reports a destination conflict.** Scaffolds refuse an existing
destination by default. Keep the existing file, choose a new target, or ask
for a deliberate manual resolution after reviewing the conflict. Do not add
an overwrite workaround to the application.

**A test fails.** Ask Pi to read the failing assertion and the relevant source,
then make the smallest behavior fix. Rerun ``python -m pytest`` and repeat the
route/template inspection if the mount or exposure changed. Do not weaken the
test to match an incorrect page.

**The runtime check fails.** Use ``tgshell`` with the explicit ``test.ini``
profile and preserve the traceback. Check the route with ``tginfo`` before
changing code. A failing assertion or exception in a ``tgshell`` script is a
failed validation signal; it is not a successful shell session.

**The feature works but the diff is broad.** Stop the session and ask the
agent to keep only the controller mount, generated feature files, and focused
test changes. This tutorial is a narrow development loop, not a framework
refactor.

The resulting workflow is intentionally ordinary: a human states product
behavior, the coding-agent harness turns the request into a small change, and
TurboGears' inspection, scaffolding, tests, and loaded runtime provide visible
checks at each step.
