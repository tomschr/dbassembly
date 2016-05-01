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

from lxml.etree import QName


NS = dict(DB="http://docbook.org/ns/docbook",
          XL="http://www.w3.org/1999/xlink",
          XI="http://www.w3.org/2001/XInclude",
          )


def db(tag):
    """Creates a DocBook 5 tag name in Clark notation

    >>> db("book")
    '{http://docbook.org/ns/docbook}book'

    :param str tag: name of tag
    :return: DocBook5 tag name string
    :rtype: str
    """
    return '{{{}}}{}'.format(NS['DB'], tag)

ASSEMBLY_TAG = QName(db('assembly'))
RESOURCES_TAG = QName(db('resources'))
STRUCTURE_TAG = QName(db('structure'))
