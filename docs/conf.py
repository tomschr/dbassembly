# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
#    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
#    'sphinxcontrib.spelling',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxcontrib.programoutput',
]
if os.getenv('SPELLCHECK'):
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
author_email = '<toms@suse.de>'
copyright = '{0}, {1}'.format(year, author)
version = release = '0.1.3'

github_project = "tomschr/dbassembly"
github_url = "https://github.com/{}".format(github_project)

pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('{}/issues/%s'.format(github_url), '#'),
    'pr': ('{}/pull/%s'.format(github_url), 'PR #'),
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

rst_epilog = """
.. |author| replace:: {author}
.. |author_email| replace:: {author_email}
.. |github_url| replace:: {github_url}
""".format(author=author,
           author_email=author_email,
           github_url=github_url,
           )
