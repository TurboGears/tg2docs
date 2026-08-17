.. _tg-agent-tooling:

==============
Agent Tooling
==============

TurboGears 2.5 devtools ship agent-oriented facilities that make a project
inspectable and safely operable by coding agents: the ``tginfo`` static
inspection command, the ``tgskills`` skill installer, and three Agent Skills.
Quickstarted projects also receive an ``AGENTS.md`` that points agents at
these tools and at version-matched reference documentation.

Project commands such as ``tginfo`` and ``tgshell`` are contributed by the
project itself. Install the generated project into the active environment
before using them::

    $ cd myproject
    $ python -m pip install -e .

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

With ``--json`` the output follows a stable contract:

- a single JSON document on stdout; application import/startup log lines go
  to stderr, so stdout can be parsed directly;
- keys are sorted and rows are deterministically ordered — output is
  byte-stable across runs for the same project;
- exit codes: ``0`` success; ``1`` missing subcommand; ``2`` unknown
  subcommand or not run inside the project; ``4`` config file load failure.
  Treat any nonzero exit as failure;
- no credentials are ever emitted: database info is ``{enabled, orm}`` and
  auth info is ``{enabled}`` only;
- source locations are relative to the project root.

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

Installation links the skills from the installed devtools package when
possible and falls back to copying; existing skill directories are never
overwritten, and symlinks escaping the project are rejected. The quickstart
installs the default target automatically. Generated projects ignore
``.agents/`` and ``.claude/`` in Git, since the skills are machine-local and
regenerated from the installed devtools version.

Agent Skills
============

The installed skills are Markdown guidance that teaches agents the
TurboGears workflow:

- ``tg-inspect`` — discovering routes, controllers, models, templates, and
  project facts through ``tginfo``;
- ``tg-scaffold`` — creating conventional project files with
  ``gearbox scaffold``, including multi-scaffold feature generation
  (``gearbox scaffold model controller template article``) and migration
  generation via ``gearbox migrate autogenerate``;
- ``tg-shell`` — running code in the fully loaded application context,
  including WebTest requests, through ``gearbox tgshell``.

The commands these skills document are the ones described in this manual;
the skills themselves are the live reference installed with the project.

Generated ``AGENTS.md``
=======================

Quickstart generates an ``AGENTS.md`` in the project root that instructs
agents to use the skills above, documents the read-only ``tginfo`` workflow,
the test discovery command (``python -m pytest --collect-only -q``), the
migration status check, and the config profiles (``development.ini`` for
development, ``test.ini`` for tests). It also embeds version-anchored
reference documentation URLs:

- https://turbogears.readthedocs.io/en/development/reference/reference.html
  for development installs;
- https://turbogears.readthedocs.io/en/latest/reference/reference.html for
  released installs.

The reference section is the entry point for configuration options, runtime
topics, and the Classes and Functions API reference; pick the URL matching
the installed TurboGears version.
