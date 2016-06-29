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
import sys

from lxml import etree

from .assembly import assembly, loadassembly


class App(object):
    """Context App-class
    """
    def __init__(self, args=None):
        """Constructor

        :param dict args: Dictionary which contains at least
          the followin keys:
          '<assembly>': a filename to the assembly XML file
          '<output>: None, a string, or a file-like object
        """
        self.xml, self.root = None, None
        self.args = {} if args is None else args
        self.assembly = self.args.get('<assembly>')
        # Option <output> can be None (=sys.stdout, the default),
        # a string, or a file-like object
        if self.args.get('--output') is None:
            self.output = sys.stdout
        elif isinstance(self.args.get('--output'), str):
            out = self.args.get('--output')
            if os.path.exists(out):
                raise FileExistsError("File %r already exists" % out)
            self.output = open(out, 'w')
        else:
            # Assume it's a file-like object
            self.output = self.args.get('--output')

    def loadassembly(self):
        """Load assembly file
        """
        self.xml = loadassembly(self.assembly)
        self.root = self.xml.getroot()

    def process(self):
        """Process the assembly file
        """
        self.loadassembly()
        result = assembly(self.xml, self.output)
        # We need [0] here to remove the root element 'realized_doc'
        self.output.write(etree.tostring(result[0],
                                         pretty_print=self.args.get('--pretty-print'),
                                         # xml_declaration=True,
                                         encoding='unicode',
                                         )
                          )
        return 0

    def __repr__(self):
        return "<%s: %r -> %r>" % (self.__class__.__name__,
                                   self.assembly,
                                   self.output,
                                   )
