# -*- coding: utf-8 -*-
"""
    TurboGears Code Documentation Extensions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Extensions to improve documentation management and effectiveness.

    These are the features implemented (see http://tinyurl.com/38ljs55):

    * Include external resources
      - From local files
      - From sections of local files
      - From a VCS (revision or tag), Subversion, Mercurial, Git, Bazaar supported via pyvcs
    * Test sample projects
    * Compress sample projects

    :copyright: Copyright 2008 by Bruno Melo.
    :license: MIT.
"""

import re
import os
import sys
import zipfile
import string

import dulwich

from docutils import nodes, utils
from docutils.parsers.rst import directives, roles, states
from docutils.statemachine import ViewList

from dulwich.client import get_transport_and_path
from pyvcs.backends import get_backend

from sphinx import util

import nose


beginmarker_re = re.compile(r'##\{(?P<section>.+)}')
endmarker_re = re.compile(r'##')
already_pulled = False

# This is based on 'Multi-line string block formatting' recipe by Brett Levin
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/145672
def format_block(block):
    """Format the given block of text, trimming leading/trailing
    empty lines and any leading whitespace that is common to all lines.
    The purpose is to let us list a code block as a multiline,
    triple-quoted Python string, taking care of indentation concerns."""
    # separate block into lines
    lines = str(block).split('\n')
    # remove leading/trailing empty lines
    while lines and not lines[0]:  del lines[0]
    while lines and not lines[-1]: del lines[-1]
    # look at first line to see how much indentation to trim
    ws = re.match(r'\s*',lines[0]).group(0)
    if ws:
        lines = map( lambda x: x.replace(ws,'',1), lines )
    return '\n'.join(lines)+'\n'

def search(source, section):
    """Search in `source` for a section as specified in markers ##{section}
    (begin marker) and ## (end marker) and extract the lines between them.
    """
    lineno = 0
    begin, end = 0, 0
    for line in source:
        if not begin:
            result = beginmarker_re.search(line)
            if result and result.group('section') == section:
                begin = lineno + 1
        elif not end:
            if beginmarker_re.search(line) or endmarker_re.search(line):
                end = lineno
        lineno += 1
    if not end:
        end = len(source)

    return '\n'.join([source[line] for line in xrange(begin, end) \
                    if not (beginmarker_re.search(source[line]) \
                            or endmarker_re.search(source[line])) ])

def localgitpath(state):
    e = state.document.settings.env
    basepath = os.sep.join(os.path.split(e.doctreedir)[:-1])
    path = os.path.join(basepath, 'gitclone')

    return path

def clone_and_pull(state, path=None):
    """Clone code_url to path"""
    global already_pulled
    if already_pulled:
        return
    
    e = state.document.settings.env
    if not path:
        path = localgitpath(state)

    client, host_path = get_transport_and_path(e.config.code_url)

    if not os.path.exists(path):
        os.mkdir(path)
        r=dulwich.repo.Repo.init(path)
    else:
        r=dulwich.repo.Repo(path)
        
    remote_refs = client.fetch(host_path, r, determine_wants=r.object_store.determine_wants_all, progress=None)
    r['HEAD'] = remote_refs['HEAD']

    already_pulled = True

def get_file(state, path, revision = None, repository = None):
    """ Read file from git repository. """
    clone_and_pull(state)
    git = get_backend('git')
    repo = git.Repository(localgitpath(state))
    data = repo.file_contents(path, revision).splitlines()
    return data

def list_files(state, path='', repo=None):
    """ list all files and folders in the repository """
    if not repo:
        git = get_backend('git')
        repo = git.Repository(localgitpath(state))
    files, folders = repo.list_directory(path)
    if path:
        rpath = '%s/' % (path)
    else:
        rpath = ''
    files = ['%s%s' % (rpath, f) for f in files]
    for f in folders:
        if path:
            rpath = '%s/%s' % (path, f)
        else:
            rpath = f
        files.extend(list_files(state, rpath, repo))
    return files
    
def code_directive(name, arguments, options, content, lineno,
                        content_offset, block_text, state, state_machine):
    """ Directive to handle code sample related stuf   """
    clone_and_pull(state)
    if not state.document.settings.file_insertion_enabled:
        return [state.document.reporter.warning('File insertion disabled',
                                                line=lineno)]
    environment = state.document.settings.env
    file_name = arguments[0]

    try:
        if options.has_key('revision'):
            revision = options['revision']
        else:
            revision = None
        data = get_file(state, file_name, revision,
                        environment.config.code_path)
        if options.has_key('section'):
            sections = [x.strip() for x in options['section'].split(',')]
            res = []
            for section in sections:
                res.extend(format_block(search(data, section)))
                res.extend('')
            source = '\n'.join(data)
        else:
            source = format_block('\n'.join(data))
        retnode = nodes.literal_block(source, source)
        retnode.line = 1
    except Exception, e:
        retnode = state.document.reporter.warning(
            'Reading file %r failed: %r' % (arguments[0], str(e)), line=lineno)
    else:
        if options.has_key('test'):
            test = options['test']
            if test.startswith(os.sep):
                result = nose.run(argv = [__file__, test])
            else:
                result = nose.run(argv = [__file__
                                          , os.path.join(environment.config.test_path
                                          , test)])
            if not result:
                retnode = state.document.reporter.warning(
                    'Test associated to %r failed' % (file_name,),
                    line=lineno)
        if options.has_key('language'):
            retnode['language'] = options['language']
    return [retnode]


def test_directive(name, arguments, options, content, lineno,
                        content_offset, block_text, state, state_machine):
    """ Directive to test code from external files """
    clone_and_pull(state)
    environment = state.document.settings.env

    test = arguments[0]
    if not test.startswith(os.sep):
        test = os.path.join(environment.config.test_path, test)

    if options.has_key('options'):
        opts = options['options'].split(',')
        # adjust the options to nose
        opts = map(lambda s: "--%s" % s.strip(), opts)

        opts.append(test)
    else:
        opts = [test]

    opts.insert(0, __file__)
    result = nose.run(argv = opts)
    if not result:
        retnode = state.document.reporter.warning(
                'Test %r failed' % (test,),
                line=lineno)
        return retnode
    return

def archive_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    archive = options['archive']
    return [nodes.reference(rawtext, utils.unescape(text), refuri=archive,
                            **options)], []

role_name = 'arch'

def archive_directive(name, arguments, options, content, lineno,
         content_offset, block_text, state, state_machine):
    """ Directive to create a archive (zip) from a sample project """
    clone_and_pull(state)
    environment = state.document.settings.env

    static_path = environment.config.html_static_path[0]

    directory = arguments[0]

    if options.has_key('file'):
        filename = options['file']
    else:
        filename = os.path.basename(directory.rstrip(os.sep)) + '.zip'

    archive_file = zipfile.ZipFile(os.path.dirname(os.path.abspath(__file__))
                        + '%s%s%s' % (os.sep, static_path, os.sep)
                        + filename, "w")

    if options.has_key('root'):
        base = options['root']
    else:
        base = ''

    fnames = list_files(state, base)
    for name in fnames:
        archive_file.writestr(name, '\n'.join(get_file(state, name)))

    archive_file.close()

    archive = util.relative_uri(state_machine.document.current_source,
                                os.path.dirname(os.path.abspath(__file__))
                        + '%s%s%s' % (os.sep, static_path, os.sep)) \
                        + filename

    role = roles.CustomRole(role_name, archive_role,
                            {'archive' : archive},
                            content)
    roles.register_local_role(role_name, role)
    return []


def setup(app):
    code_options = {'section': directives.unchanged,
                    'language': directives.unchanged,
                    'test': directives.unchanged,
                    'revision': directives.unchanged}
    test_options = {'options': directives.unchanged}
    archive_options = {'file': directives.unchanged,
                       'root': directives.unchanged}

    app.add_config_value('code_url', '', True)
    app.add_config_value('code_path', '', True)
    app.add_directive('code', code_directive, 1, (1, 0, 1),  **code_options)

    app.add_directive('test', test_directive, 1, (1, 0, 1),  **test_options)
    app.add_config_value('test_path', '', True)

    app.add_directive('archive', archive_directive, 1, (1, 0, 1), **archive_options)

