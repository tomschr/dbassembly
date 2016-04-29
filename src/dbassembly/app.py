#
# Copyright (c) 2016 SUSE Linux GmbH.  All rights reserved.
#
# This file is part of dbassembly.
#
# kiwi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kiwi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kiwi.  If not, see <http://www.gnu.org/licenses/>
#

from lxml import etree
from .logger import log


class App(object):
    def __init__(self, args=None):
        self.args = {} if args is None else args
        self.assembly = self.args.get('<assembly>')

    def process(self):
        log.debug("process called")

    def __repr__(self):
        return repr(self.args)


