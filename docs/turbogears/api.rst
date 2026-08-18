.. _api-tutorial:

============================
Building a JSON API
============================

TurboGears 2.5 ships a dedicated quickstart for JSON APIs: ``gearbox
quickstart-api`` creates a project with REST controllers, automatic parameter
validation, JSON error responses, an automatically generated `OpenAPI
<https://spec.openapis.org/>`_ specification, interactive API documentation,
and optional Bearer-token authentication.

This tutorial walks through the generated project and shows how to build on
it: a validated, OpenAPI-compatible JSON API over a movie catalog.

Creating the project
====================

Create a new API project and install it::

    $ gearbox quickstart-api myproject --auth --sqlalchemy
    $ cd myproject
    $ python -m pip install -e '.[development]'

``--auth`` adds authentication (Bearer tokens and cookie login), and
``--sqlalchemy`` selects SQLAlchemy as the ORM. ``--ming`` selects MongoDB
via Ming and ``--nosa`` skips the database entirely; omit ``--auth`` for an
unauthenticated API. The quickstart also installs the coding-agent skills
into ``.agents/skills/`` and generates an ``AGENTS.md`` describing the
project workflow — see :ref:`tg-agent-tooling`.

Initialize the database (creates the schema plus demo users and sample
movies) and start the development server::

    $ gearbox setup-app -c development.ini
    $ gearbox serve -c development.ini --reload

The development database lives in ``devdata.db`` next to
``development.ini``; ``test.ini`` uses an in-memory database for tests.

What was generated
==================

The interesting parts of the generated project:

- ``<package>/controllers/api/__init__.py`` — the ``APIController`` mounted
  at ``/api``; it exposes ``index`` (API summary), ``openapi`` (the OpenAPI
  specification) and ``docs`` (interactive Redoc documentation);
- ``<package>/controllers/api/movies.py`` — ``MoviesController``, a
  :ref:`RestController <restdispatch>` implementing the movie catalog;
- ``<package>/model/movie.py`` — the ``Movie`` model with its
  ``__API_SCHEMA__`` (the OpenAPI schema of the resource) and ``__json__``
  (how the model is serialized);
- ``<package>/tests/functional/`` — WebTest tests for the movies API and
  for authentication.

The API in action
=================

With the server running, the catalog endpoints behave like this::

    $ curl http://127.0.0.1:8080/api/movies
    {"movies": [{"id": "1", "title": "Inception", "year": 2010, ...}]}

    $ curl -X POST -H 'Content-Type: application/json' \
        -d '{"title": "Arrival", "year": 2016, "description": "First contact"}' \
        http://127.0.0.1:8080/api/movies
    {"movie": {"id": "4", "title": "Arrival", "year": 2016, ...}}   [201]

    $ curl -X PUT -H 'Content-Type: application/json' \
        -d '{"title": "Arrival", "description": "Science fiction"}' \
        http://127.0.0.1:8080/api/movies/4
    {"movie": {"id": "4", "title": "Arrival", ...}}                 [200]

    $ curl -X DELETE http://127.0.0.1:8080/api/movies/4
    {"status": "deleted", "movie_id": "4"}                          [200]

``POST`` returns ``201``; unknown movies return ``404``. The generated
``tests/functional/test_movies.py`` exercises the full CRUD cycle.

Validation
==========

The controller signatures drive validation. In ``movies.py`` the
``post`` action declares its parameters as type hints::

    @expose('json')
    @validate(error_handler=validation_errors_response)
    def post(self, title: str, year: int = None, description: str = None, **kw):
        """Add a movie to the catalog. ..."""
        movie = Movie(title=title, year=year, description=description)
        DBSession.add(movie)
        DBSession.flush()
        response.status_int = 201
        return dict(movie=movie)

``@validate`` without explicit validators builds them from the signature:
``title: str`` is a required string, ``year: int = None`` is an optional
integer. This is a TurboGears 2.5 feature — type hints become runtime
validation.

Send invalid data and the API answers in JSON::

    $ curl -X POST -H 'Content-Type: application/json' -d '{}' \
        http://127.0.0.1:8080/api/movies
    [400]                                       # missing required "title"

    $ curl -X POST -H 'Content-Type: application/json' \
        -d '{"title": "Arrival", "year": "soon"}' http://127.0.0.1:8080/api/movies
    {"errors": {"year": "Invalid"},
     "values": {"title": "Arrival", "year": "soon"}}            [422]

The two failure modes are distinct:

- a *missing* required parameter fails the REST signature match and returns
  ``400 Bad Request`` (send ``Accept: application/json`` to get the error
  as JSON instead of HTML);
- a *present but invalid* value is rejected by the validators and returned
  through ``validation_errors_response`` as ``422 Unprocessable Content``
  with an ``{"errors": {...}, "values": {...}}`` body.

JSON request bodies are decoded automatically because the generated
``app_cfg.py`` sets ``decode_json_params: True`` — the request body is
merged with the URL and form parameters before validation.

You can go beyond type hints by passing explicit validators to
``@validate`` (see the :ref:`validation documentation <validation>`), and
restrict which HTTP methods may reach an action with the 2.5.1
``allowed_methods`` option::

    @expose('json', allowed_methods=['GET', 'POST'])
    def catalog(self, **kw):
        ...

Disallowed methods receive ``405 Method Not Allowed`` with an ``Allow``
header.

JSON responses and errors
=========================

``@expose('json')`` serializes the returned dict with the JSON renderer;
models are serialized through their ``__json__`` method, so you control the
wire format (the generated ``Movie.__json__`` returns the id as a string).

HTTP errors are also JSON when the client asks for it::

    $ curl -H 'Accept: application/json' http://127.0.0.1:8080/api/movies/99999
    {"message": "The resource could not be found.<br /><br />\n\n\n",
     "code": "404 Not Found", "title": "Not Found"}             [404]

In controller code, ``abort(404, "Movie not found")`` raises the error;
``abort`` also supports ``passthrough="json"`` for a compact JSON body.

OpenAPI specification
=====================

The API is OpenAPI-compatible out of the box. ``tgext.apispec`` builds the
specification from the controllers::

    $ curl http://127.0.0.1:8080/api/openapi.json

The generated document includes one path per exposed action. Its content is
driven by the action docstrings, which embed OpenAPI fragments — tags,
responses and content schemas::

    @expose('json')
    def get_all(self, **kw):
        """Return the movies available in the catalog.

        Each movie includes its title, release year, and description.

        ---
        tags: [movies]
        responses:
          200:
            description: List of all movies
            content:
              application/json:
                schema:
                  type: object
                  required: [movies]
                  properties:
                    movies:
                      type: array
                      items:
                        $ref: '#/components/schemas/Movie'
        """
        movies = DBSession.query(Movie).all()
        return dict(movies=movies)

The ``requestBody`` schema of ``POST /api/movies`` is generated from the
action's type hints (title required, year integer, description string), so
the specification and the runtime validation stay in sync. Model schemas
are contributed through ``__API_SCHEMA__`` on the model class and appear
under ``components/schemas``.

Point a browser at ``http://127.0.0.1:8080/api/docs`` for the interactive
Redoc documentation of the same specification.

Adding endpoints
================

To add a resource, create a new REST controller next to ``movies.py`` and
mount it in ``APIController``::

    class BooksController(RestController):
        @expose('json')
        def get_all(self, **kw):
            """List all books.

            ---
            tags: [books]
            responses:
              200:
                description: List of books
            """
            return dict(books=[...])

    class APIController(BaseController):
        """API root controller."""

        movies = MoviesController()
        books = BooksController()

The new endpoints appear automatically in ``/api/openapi.json`` and in the
Redoc page — no spec file to maintain. ``gearbox scaffold`` can generate
model, controller and template skeletons for you (see the
:ref:`scaffolding documentation <scaffolding>`).

Authentication
==============

With ``--auth`` the API supports two authentication methods:

**Bearer tokens** — send the token in the ``Authorization`` header::

    $ curl -H 'Authorization: Bearer abc123def456ghi789jkl012mno345' \
        http://127.0.0.1:8080/demo/admin
    {"message": "Welcome, admin!", "status": "ok", "user": "manager"}

The generated ``app_cfg.py`` registers a ``BearerTokenIdentifier`` repoze.who
plugin that turns the header into an identity, plus a dedicated
``BearerTokenAuthenticator`` that resolves the token against the
``api_token`` column of the user table. Standard username/password login is
left untouched.

**Cookie login** — the standard TurboGears form flow::

    $ curl -c cookies.txt -X POST \
        -d 'login=manager&password=managepass' http://127.0.0.1:8080/login_handler
    $ curl -b cookies.txt http://127.0.0.1:8080/demo/admin
    {"message": "Welcome, admin!", "status": "ok", "user": "manager"}

The same flow protects web pages. Open ``http://127.0.0.1:8080/secure`` in a
browser while logged out: you are redirected to the login page, and after
signing in with ``manager``/``managepass`` you land back on the protected
page showing your name. The page is the ``secure`` action of the root
controller, guarded by ``predicates.not_anonymous`` — the showcase to copy
when you need login-protected HTML pages next to your API.

The demo users are created by ``gearbox setup-app``: ``manager``
(password ``managepass``, token ``abc123def456ghi789jkl012mno345``, has the
``manage`` permission) and ``editor`` (password ``editpass``, token
``pqr678stu901vwx234yz567abc890``). Protect actions with ``@require`` and
predicates::

    @expose('json')
    @require(predicates.has_permission('manage', msg=l_('Requires manage permission')))
    def admin(self, **kw):
        ...

Unauthenticated requests are redirected to the login page; API clients
should treat any non-``2xx`` response as a failure and re-authenticate.

Tests
=====

The generated project ships a WebTest suite::

    $ python -m pytest

It covers the movies CRUD cycle, the validation status codes (400, 422,
404), the OpenAPI endpoints, and authentication (Bearer and cookie login).
``tests/functional/test_auth.py`` shows how to create users and
permissions in the test database.

Next steps
==========

- Read the generated ``README.rst`` for the full endpoint list and the
  cleanup instructions (the demo controller, model and movies API can be
  removed once you start your own resource);
- :ref:`restdispatch` covers RestController in depth;
- the :ref:`validation documentation <validation>` covers validators and
  error handling beyond type hints;
- :ref:`tg-agent-tooling` documents ``tginfo`` and the Agent Skills that
  inspect this project.
