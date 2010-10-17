# -*- coding: utf-8 -*-
#
# TG2 documentation build configuration file, created by
# sphinx-quickstart on Sat May  3 11:00:38 2008.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# All configuration values have a default value; values that are commented out
# serve to show the default value.

import sys, os
from tg.release import version as tg_release_version
from pkg_resources import get_distribution, VersionConflict

# If your extensions are in another directory, add it here. If the directory
# is relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.todo', 'code_ext']

todo_include_todos = True

#add inter-sphinx crosslinks here
intersphinx_mapping = {'http://docs.python.org/dev': None,
                       'http://www.pylonshq.com/docs/en/0.9.7/':None,
                       'http://www.sqlalchemy.org/docs/05/':None,
                       'http://sprox.org/': None,
                       'http://docs.python-rum.org/':None,
                       'http://toscawidgets.org/documentation/tw.forms/':None,
                       'http://toscawidgets.org/documentation/ToscaWidgets/':None,
                       }

# The maximum number of days to cache remote inventories.
# The default is 5, meaning five days.
# Set this to a negative value to cache inventories for unlimited time.
#
#intersphinx_cache_limit = 5

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'toc'

# General substitutions.
project = 'TG2'
copyright = '2009-2010, TurboGears DocTeam'

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version.
version = '2.1rc1'
# The full version, including alpha/beta/rc tags.

release = tg_release_version

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
# unused_docs = []

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'default'


# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_style = 'tg.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# The name of an image file (within the static path) to place at the top of
# the sidebar.
html_logo = 'tg.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.
#html_use_opensearch = False

# Output file base name for HTML help builder.
htmlhelp_basename = 'TG2doc'

# Options for epub output
# -----------------------
epub_basename = 'TurboGears_2.1'
epub_title = 'TurboGears Documentation for Version ' + release
epub_author = 'TurboGears Documentation Team'
epub_language = 'en'
epub_publisher = 'TurboGears'
epub_identifier = 'http://www.turbogears.org/'
epub_scheme = 'URL'
epub_pre_files = []
epub_post_files = []
epub_exclude_files = ['_downloads/ToscaSample-0.2dev.zip', '_static/doctools.js', '_static/underscore.js',
                      '_static/screenshot.tiff', '_static/searchtools.js', '_static/turbogears.pdf',
                      '_static/ToscaWidgetsFormsExample.zip', '_static/trunk.zip', '_static/jquery.js',
                      '_static/Wiki20_final.zip', '_static/tutorials/Helloworld.zip', '_static/tutorials/Wiki-20.zip',
                      '_static/tutorials/sqlautocode/moviedemo.db'
                      ]
epub_tocdepth = 2

# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
latex_documents = [
  ('index', 'TG2.tex', 'TG2 Documentation', 'TurboGears DocTeam', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True

code_scm = 'svn'
code_path = test_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'project_code' + os.path.sep

# We can't build the docs with older Sphinx and the error that is
# shown is not helpful at all so we print something better.
def check_sphinx_vers():
    min_vers = "0.6.4"
    try:
        get_distribution("sphinx >= %s" % min_vers)
    except VersionConflict:
        sys.stderr.write("Your version of Sphinx is too old. "
                         "Please upgrade to Sphinx %s or later.\n" % min_vers)
        sys.exit(1)

check_sphinx_vers()
