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

from functools import wraps


class raises(object):
    """
    exception decorator as used in nose, tools/nontrivial.py
    """
    def __init__(self, *exceptions):
        self.exceptions = exceptions
        self.valid = ' or '.join([e.__name__ for e in exceptions])

    def __call__(self, func):
        name = func.__name__

        def newfunc(*args, **kw):
            try:
                func(*args, **kw)
            except self.exceptions:
                pass
            except:
                raise
            else:
                message = "%s() did not raise %s" % (name, self.valid)
                raise AssertionError(message)
        newfunc = wraps(func)(newfunc)
        return newfunc
