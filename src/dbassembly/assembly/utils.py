#
# Copyright (c) 2016 SUSE Linux GmbH.  All rights reserved.
#
# This file is part of dbassembly.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

import os
from urllib.parse import urljoin, urlparse

from ..core import ATTRS_NOT_COPIED
from ..logger import log


def getxmlbase(base, path):
    """Determine base path; if path is absolute, return
       this absolute path instead of base from tree

    :param str base: base URL from ElementTree
    :param str path: relative source
    :return: string of concatenated base and relative part

    >>> getxmlbase("http://www.example.org/", "foo/path")
    'http://www.example.org/foo/path'
    >>> getxmlbase("http://www.example.org/", "file:foo/path")
    'http://www.example.org/foo/path'
    >>> import os; os.chdir("/usr")
    >>> getxmlbase("", "bin/ls")
    '/usr/bin/ls'
    >>> getxmlbase("bin", "ls")
    '/usr/bin/ls'
    >>> getxmlbase("bin/", "ls")
    '/usr/bin/ls'
    >>> getxmlbase("bin/", "./ls")
    '/usr/bin/ls'
    >>> getxmlbase("bin", "/tmp/foo")
    '/tmp/foo'
    >>> getxmlbase(None, "/tmp/foo")
    '/tmp/foo'
    >>> getxmlbase(".", None)
    '/usr/'
    """
    b = urlparse(base)
    p = urlparse(path)
    # Check if we have a local path:
    if b.scheme == '':
        # "/" at the end needed for urljoin
        base = os.path.abspath(base) + "/"
    if p.scheme == 'file':
        path = p.path

    return urljoin(base, path)


def matchesformats(outputformat, targetformats, sep=";"):
    """Checks if one of the outputformat is available in targetformat

    >>> matchesformats('foo', ['html', 'pdf'])
    False
    >>> matchesformats('pdf', ['html', 'pdf'])
    True
    >>> matchesformats('pdf;html', ['html', 'pdf'])
    True
    >>> matchesformats('html;pdf', ['html', 'pdf'])
    True
    >>> matchesformats('', ['html', 'pdf'])
    True
    >>> matchesformats(';', ['html', 'pdf'])
    False
    >>> matchesformats(None, ['html', 'pdf'])
    True

    :param outputformat: string with optional ";" as delimiters
    :param targetformats: list of target format strings
    :param sep: separator where to split outputformat
    :return: True, if one of the outputformat is available in targetformat,
             False otherwise
    :rtype:  bool
    """
    if outputformat is None or outputformat == '':
        return True
    if targetformats is None:
        return False

    oformats = set(outputformat.split(sep))
    tformats = set(targetformats)
    return bool(oformats & tformats)


def parse_chunk(element):
    """Return an elements @chunk attribute

    :param element: Element
    :return: True, False, or None
    """
    mapping = {'true': True,
               'false': False,
               'auto': None,
               }
    chunk = element.attrib('chunk')
    if chunk not in mapping:
        log.warning("Invalid value %r in chunk attribute. "
                    "Falling back to 'auto'.",
                    chunk
                    )
        # return None
    return mapping.get(chunk)


def copy_module_attributes(realized, module_or_struct):
    """Copy all attributes into the realized document (except those
       from ATTRS_NOT_COPIED)

    :param realized: Element
    :param module_or_struct: Element
    """
    for attrib, value in module_or_struct.attrib.items():
        if attrib not in ATTRS_NOT_COPIED:
            realized.attrib[attrib] = value
