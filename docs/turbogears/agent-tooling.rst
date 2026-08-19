.. _tg-agent-tooling:

==============
Agent Tooling
==============

TurboGears 2.5 devtools provide project-aware tooling for developers who work
with coding agents: the ``tginfo`` static inspection command, the ``tgskills``
skill installer, and three Agent Skills. Full-stack and API quickstarts also
receive an ``AGENTS.md`` with project-local workflow and version-matched
reference links.

This is optional development tooling. A generated application's runtime does
not depend on the coding-agent tools.

Project commands such as ``tginfo`` and ``tgshell`` are contributed by the
project itself. Install the generated project with its development extra into
the active environment before using them::

    $ cd myproject
    $ python -m pip install -e '.[development]'

``tginfo`` — Static project inspection
======================================

``gearbox tginfo`` reports read-only, structured facts about a project.
Select the profile explicitly and run it from the project root::

    $ gearbox tginfo summary --project . --config development.ini --json

Selectors:

- ``summary`` — package name, default renderer and renderers, paths, root
  controller, database (enabled/ORM kind), auth (enabled);
- ``routes`` — flat route/action rows: path, kind (controller, action,
  dynamic lookup/default), controller and action fully-qualified names and
  source locations, docstrings, params, validations, exposures (renderer,
  content type, template);
- ``models`` — exported model classes: name, class, module, source, ORM kind
  (sqlalchemy/ming/unknown), docstring;
- ``templates`` — recognized template files: dotted name, path, renderer,
  and the route paths exposing each template;
- ``scaffolds`` — scaffold templates available to ``gearbox scaffold``.

Omit ``--json`` for human-readable output.

JSON output contract
--------------------

Use ``--json`` when the output will be consumed by another tool or a coding
agent. The command writes one JSON document to stdout and diagnostics to
stderr. Treat any nonzero exit code as failure. The output omits credentials
and reports source locations relative to the project root.

The current exit codes are ``0`` for success, ``1`` for a missing subcommand,
``2`` for an unknown subcommand or a command run outside a project, and ``4``
for a configuration-file load failure.

Safety
------

``tginfo`` is read-only, but loading application code can execute
project-defined import, startup, and request-hook code, like any Python
import. Do not run ``setup-app`` or migration upgrades as part of routine
inspection; for a read-only migration status check use::

    $ gearbox migrate -c development.ini db_version

``tgskills`` — Agent skill installation
=======================================

``gearbox tgskills`` installs the Agent Skills into the current project::

    $ gearbox tgskills

- by default skills are installed under ``.agents/skills/``;
- ``--claude`` installs only ``.claude/skills/`` for Claude Code.

The quickstart installs the default target automatically. Running the
installer again does not replace an existing skill directory. The skill files
are machine-local and generated projects ignore ``.agents/`` and
``.claude/`` in Git. Use ``--claude`` when the project is being used with
Claude Code; otherwise the default ``.agents/skills/`` target is appropriate.

Agent Skills
============

The installed skills are Markdown guidance for project-aware development:

- ``tg-inspect`` — discovering routes, controllers, models, templates, and
  project facts through ``tginfo``;
- ``tg-scaffold`` — creating conventional project files with
  ``gearbox scaffold``, including multi-scaffold feature generation
  (``gearbox scaffold model controller template article``) and migration
  generation via ``gearbox migrate autogenerate``;
- ``tg-shell`` — running code in the fully loaded application context,
  including WebTest requests, through ``gearbox tgshell``.

Working with a coding agent
===========================

TurboGears tooling does not decide what an application should do. A human
still provides the product behavior, constraints, and acceptance checks. The
tooling makes the existing project easier to understand and gives the human
visible checks around an agent's changes:

- use ``tginfo`` to inspect the project before relying on assumptions about
  routes, models, templates, or available scaffolds;
- use ``tg-scaffold`` when new files should follow project conventions;
- review the generated and edited diff before accepting it, especially before
  running setup or migration commands;
- run the project's tests, then use ``tg-shell`` for a loaded-application or
  WebTest check when static inspection is not enough.

Keep the boundaries clear: ``tginfo`` describes project structure,
``tg-scaffold`` writes project files, and ``tg-shell`` executes application
code. For a complete worked example, see :ref:`tg-agentic-development`.

Generated ``AGENTS.md``
=======================

Quickstart generates an ``AGENTS.md`` in the project root as a project-local
handoff document. Read it before working with an agent. It identifies the
skills, documents the read-only ``tginfo`` workflow, the test discovery
command (``python -m pytest --collect-only -q``), the migration status check,
and the config profiles (``development.ini`` for development, ``test.ini``
for tests). It also embeds version-anchored reference documentation URLs:

- https://turbogears.readthedocs.io/en/development/reference/reference.html
  for development installs;
- https://turbogears.readthedocs.io/en/latest/reference/reference.html for
  released installs.

The reference section is the entry point for configuration options, runtime
topics, and the Classes and Functions API reference; pick the URL matching
the installed TurboGears version.
