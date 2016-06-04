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

from lxml import etree

from .core import (RESOURCE_TAG,
                   RESOURCES_TAG,
                   STRUCTURE_TAG,
                   XMLID,
                   XMLLANG,
                   )
from .exceptions import (MissingAttributeRessource,
                         NoStructure,
                         ResourceNotFoundError)
from .logger import log


def handleitem(item, position):
    """Handle item and return content of href attribute

    :param item: Element object
    :param tuple position: current position of current
        <resources> element and <resource> element
        (starting both from 1)
    :return: string content of href attribute or exception
    :throws: MissingAttributeRessource
    """
    xmlid = item.attrib.get(XMLID)
    href = item.attrib.get('href')
    error = 1 if href is None else 0
    error += 1 if xmlid is None else 0
    if error > 0:
        name = 'href' if href is None else 'xml:id'
        msg = 'Missing %s in resources[%i]/resource[%i]' % (name,
                                                            position[0],
                                                            position[1])
        try:
            description = item[0].text.strip()
            msg += ": %r" % description
        except IndexError:
            pass

        raise MissingAttributeRessource(msg)
    return xmlid, href


def getresource(tree):
    """Creates mapping between xml:id -> href

    :param tree: ElementTree to process
    :return: dictionary
    """
    resource = {}
    for i, res in enumerate(tree.iter(RESOURCES_TAG.text), 1):
        for j, item in enumerate(res.iter(RESOURCE_TAG.text), 1):
            xmlid, href = handleitem(item, (i, j))
            resource[xmlid] = href
    log.debug("Found resources: %r", resource)
    return resource


def getstructure(tree):
    """Create a list of <structure>s
    """
    structures = list(tree.iter(STRUCTURE_TAG.text))
    # TODO: Check if it is the correct structure element
    if not structures:
        raise NoStructure('No structure element found in assembly')
    return structures[0]


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


def includedoc(realized, include):
    """Append include document into realized structure

    :param realized: Element
    :param str include: path
    """
    doc = etree.parse(include)
    realized.append(doc.getroot())


def realizedoc(tree, structure, resource):
    """Create the realized document

    :param tree: ElementTree
    :param structure: Element <structure>
    :param dict resource: dictionary of xml:id -> href
    """
    realized = etree.Element("realized_doc")
    resref = structure.attrib.get('resourceref')
    if resref is not None:
        if resref not in resource:
            raise ResourceNotFoundError("Resource %r could not be found." % resref)

        p = urlparse(tree.docinfo.URL)
        include = getxmlbase(os.path.dirname(p.path), resource[resref])
        log.debug("Resource found: %r -> %r", resref, include)

        lang = structure.attrib.get(XMLLANG)
        xmlid = structure.attrib.get(XMLID)
        if lang:
            realized.attrib[XMLLANG] = lang
        if xmlid:
            realized.attrib[XMLID] = xmlid

        includedoc(realized, include)

    return realized


def assembly(tree, base_url=None):
    """Process an ElementTree

    :param tree: ElementTree to process
    :param base_url: xml:base to use if not set in the tree
    :return: new ElementTree
    """
    # step1: load the assembly file
    resource = getresource(tree)

    # step 2: find all structure elements
    structure = getstructure(tree)

    # step 3: target formats

    # step 4: parseAssembly(assembly)
    rdoc = realizedoc(tree, structure, resource)

    # step 5: create new document

    # step 6: transclusions

    # step 7: filter

    # step 8: checking realized document
    # check()

    return rdoc
