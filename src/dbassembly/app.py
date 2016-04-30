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

from . import NS
from .exceptions import NoAssemblyFileError
from .logger import log


class App(object):
    ASSEMBLY_TAG = etree.QName('{{{}}}assembly'.format(NS['DB']))

    def __init__(self, args=None):
        self.args = {} if args is None else args
        self.assembly = self.args.get('<assembly>')
        self.output = self.args.get('<output>')

    def process(self):
        log.debug("processing assembly...")
        self.xml = etree.parse(self.assembly)
        log.debug("xml %s", self.xml)
        self.root = self.xml.getroot()
        name = etree.QName(self.root)
        if name != self.ASSEMBLY_TAG:
            raise NoAssemblyFileError('Got %s' % str(name))

        return self.assembly

    def __repr__(self):
        return "<%s: %r -> %r>" % (self.__class__.__name__,
                                   self.assembly,
                                   self.output,
                                   )
