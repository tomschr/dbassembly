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

from lxml import etree

from ..core import ASSEMBLY_TAG, RESOURCE_TAG, RESOURCES_TAG, XMLID
from ..exceptions import MissingAttributeRessource, NoAssemblyFileError
from ..logger import log


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
        msg = 'Missing {} in resources[{}]/resource[{}]'.format(name, *position)
        try:
            description = item[0].text.strip()
            msg += ": %r" % description
        except IndexError:
            pass

        raise MissingAttributeRessource(msg)
    return xmlid, href


def loadassembly(assemblyfile):
    """Load assembly file and return tree

    :param str assemblyfile: assembly filename
    :return: ElementTree
    """
    parser = etree.XMLParser(encoding="utf-8",
                             ns_clean=True,
                             )
    xml = etree.parse(assemblyfile, parser)
    root = xml.getroot()
    if etree.QName(root) != ASSEMBLY_TAG:
        raise NoAssemblyFileError('Got %r element '
                                  'instead of <assembly>.' % root.tag)
    return xml


def includedoc(realized, include):
    """Append include document into realized structure

    :param realized: Element
    :param str include: path
    """
    doc = etree.parse(include)
    realized.append(doc.getroot())


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
