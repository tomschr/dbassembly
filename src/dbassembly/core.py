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

from itertools import chain
from lxml.etree import QName as _QName

__all__ = ['ATTRS_NOT_COPIED',
           'ASSEMBLY_TAG',
           'EFFECTIVITY_ATTRIBS',
           'MODULE_OR_STRUCT_ATTRIBS',
           'MODULE_TAG',
           'NSMAP',
           'OUTPUT_TAG',
           'RELATIONSHIP_TAG',
           'RESOURCES_TAG',
           'RESOURCE_TAG',
           'STRUCTURE_TAG',
           'TRANSFORMS_TAG',
           'XMLID',
           'XMLLANG',
           'QName', 'da', 'db', 'xmlattr']

# -------- Namespace mappings
NSMAP = dict(db="http://docbook.org/ns/docbook",
             # Namespace for dbassembly project ("da") itself:
             da="https://github.com/tomschr/dbassembly",
             # DocBook 5 namespace for local attributes (used in XInclude 1.1):
             local="http://www.w3.org/2001/XInclude/local-attributes",
             # DocBook 5 transclusion namespace:
             trans="http://docbook.org/ns/transclude",
             # XLink namespace:
             xlink="http://www.w3.org/1999/xlink",
             # XInclude namespace:
             xi="http://www.w3.org/2001/XInclude",
             # XML namespace (used in xml:id, xml:lang, etc.):
             xml="http://www.w3.org/XML/1998/namespace",
             )


# For compatibility reasons, older versions of lxml do not
# have/know __str__, so this is something that wouldn't be
# possible:
# >>> str(QName('{urn:xxx}transforms'))
# '{urn:xxx}transforms'
#
if not hasattr(_QName, '__str__'):
    class QName(_QName):
        __doc__ = _QName.__doc__

        def __str__(self):
            return self.text

        def __repr__(self):
            return "<%s: %r>" % (self.__class__.__name__, self.text)
else:
    # for lxml versions that provide __str__, use original name
    QName = _QName
    del _QName


# -------- Functions
def da(name):
    """Creates a DBAssembly name in Clark notation

    >>> da("base")
    '{https://github.com/tomschr/dbassembly}base'

    :param str name: name of tag
    :return: name string in Clark notation
    :rtype: str
    """
    return str(QName(NSMAP['da'], name))


def db(tag):
    """Creates a DocBook 5 tag name in Clark notation

    >>> db("book")
    '{http://docbook.org/ns/docbook}book'

    :param str tag: name of tag
    :return: DocBook5 tag name string
    :rtype: str
    """
    return str(QName(NSMAP['db'], tag))


def xmlattr(attrib):
    """Creates an XML attribute name in Clark notation

    >>> xmlattr("id")
    '{http://www.w3.org/XML/1998/namespace}id'
    >>> xmlattr("lang")
    '{http://www.w3.org/XML/1998/namespace}lang'

    :param str tag: name of tag
    :return: XML attribute name string
    :rtype: str
    """
    return str(QName(NSMAP['xml'], attrib))


# -------- Predefinied tag names
ASSEMBLY_TAG = QName(db('assembly'))
MODULE_TAG = QName(db('module'))
OUTPUT_TAG = QName(db('output'))
RELATIONSHIP_TAG = QName(db('relationship'))
RESOURCES_TAG = QName(db('resources'))
RESOURCE_TAG = QName(db('resource'))
STRUCTURE_TAG = QName(db('structure'))
TRANSFORMS_TAG = QName(db('transforms'))

# -------- Predfined attribute names
XMLID = xmlattr('id')
XMLLANG = xmlattr('lang')

# -------- DocBook's effectivity attributes
EFFECTIVITY_ATTRIBS = ("arch",
                       "audience",
                       "condition",
                       "conformance",
                       "os",
                       "revision",
                       "security",
                       "userlevel",
                       "vendor",
                       "wordsize"
                       )
MODULE_OR_STRUCT_ATTRIBS = ("chunk",
                            "contentonly",
                            "defaultformat",
                            "omittitles",
                            "renderas",
                            "resourceref",
                            "type"
                            )
ATTRS_NOT_COPIED = tuple(name for name in chain(EFFECTIVITY_ATTRIBS,
                                                MODULE_OR_STRUCT_ATTRIBS,
                                                ('outputformat',)))
del chain
