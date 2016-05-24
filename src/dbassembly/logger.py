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
#
import logging
import sys


__all__ = ['log']


log = logging.getLogger("dbasmy")


def setloglevel(verbose):
    """Set log level according to verbose argument

    :param int verbose: verbose level to set
    """
    global log
    #: Dictionary: Log levels to map verbosity level
    #: to logging values
    LOGLEVELS = {None: logging.NOTSET,
                 0: logging.NOTSET,
                 1: logging.INFO,
                 2: logging.DEBUG,
                 }
    log.setLevel(LOGLEVELS.get(verbose, logging.DEBUG))


# This is the default log level:
log.setLevel(logging.DEBUG)
_ch = logging.StreamHandler(sys.stderr)
_frmt = logging.Formatter('%(asctime)s [%(levelname)s]: '
                          '%(message)s', '%H:%M:%S')
_ch.setFormatter(_frmt)
log.addHandler(_ch)
