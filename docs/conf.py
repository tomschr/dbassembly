# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
#    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_US'
    spelling_show_suggestions = True
    spelling_ignore_acronyms = True
    spelling_ignore_importable_modules = True
    spelling_ignore_python_builtins = True
    spelling_ignore_pypi_package_names = True
    spelling_word_list_filename = 'spelling_wordlist.txt'


source_suffix = '.rst'
master_doc = 'index'
project = 'dbassembly'
year = '2016'
author = 'Thomas Schraitle'
copyright = '{0}, {1}'.format(year, author)
version = release = '0.1.0'

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/tomschr/dbassembly/issues/%s', '#'),
    'pr': ('https://github.com/tomschr/dbassembly/pull/%s', 'PR #'),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

if 'sphinx.ext.napoleon' in extensions:
    napoleon_use_ivar = True
    napoleon_use_rtype = False
    napoleon_use_param = False
