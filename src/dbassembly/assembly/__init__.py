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
from urllib.parse import urlparse

from lxml import etree

from ..core import STRUCTURE_TAG, XMLID, XMLLANG
from ..exceptions import (NoResultDocumentError,
                          NoStructure,
                          ResourceNotFoundError)
from ..logger import log
from .resource import getresource, includedoc
from .utils import getxmlbase


def findstructure(tree):
    """Create a list of <structure>s

    :param tree: ElementTree to process
    :return: first <structure> element
    """
    struct = tree.find(STRUCTURE_TAG)
    if struct is None:
        raise NoStructure('No structure element found in assembly')
    return struct


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

    # Does <realized_doc> really contain child elements? If not,
    # something went wrong, so raise an exception.
    try:
        realized[0]
    except IndexError:
        raise NoResultDocumentError("No result document created")

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
    structure = findstructure(tree)

    # step 3: target formats

    # step 4: parseAssembly(assembly)
    rdoc = realizedoc(tree, structure, resource)

    # step 5: create new document

    # step 6: transclusions

    # step 7: filter

    # step 8: checking realized document
    # check()

    return rdoc
