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

"""
Entrypoint module, in case you use :command:`python -mdbassembly`.

Why does this file exist, and why :func:`__main__`?
For more info, read:

* https://www.python.org/dev/peps/pep-0338/
* https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

from dbassembly.cli import main

if __name__ == "__main__": # noqa
    main()  # noqa
