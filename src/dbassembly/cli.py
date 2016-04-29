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
dbassembly.cli Module
=====================

Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from :func:`__main__` later, but that
  will cause problems: the code will get executed twice:

  * When you run :command:`python -mdbassembly` Python will execute
    :file:`__main__.py` as a script. That means there won't be any
    :func:`dbassembly.__main__` in :py:class:`sys.modules`.
  * When you import __main__ it will get executed again (as a module) because
    there's no :func:`dbassembly.__main__` in :py:class:`sys.modules`.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

from docopt import docopt, DocoptExit
import sys

from .app import App
from . import logger
from . import __version__, __proc__


def parsecli(argv=None):
    """Parse command line arguments with docopt

    :param list argv: Arguments to parse or None (=use `sys.argv`)
    :return: parsed arguments
    :rtype: :py:class:`docopt.Dict`
    """
    _doc = """
usage: dbassembly -h | --help
       dbassembly --version
       dbassembly [-v]... [options] [--] <assembly>

  global options:
    --version
        show program version
    -o <output> --output=<output>
        save realized DocBook document
    -b <basedir> --basedir=<basedir>
        define base directory of processing
    -f=<format> --format=<format>
        select <format> from assembly
    -v  raise verbosity
    """
    cli = docopt(_doc,
                  version='%s version %s' % (__proc__, __version__),
                  options_first=True,
                  argv=argv,
                  )
    logger.log.info("docops: %s", cli)
    logger.setloglevel(cli['-v'])
    return cli


def main(args=None):
    """Main entry point
    """
    try:
        cli = parsecli(args)
        app = App(cli)
        logger.log.debug("Hallo Welt!")
        logger.log.info("app=%s", app)
    except KeyboardInterrupt:
        logger.log.error('%s aborted by keyboard interrupt' % __proc__)
        sys.exit(1)
    except DocoptExit as error:
        # exception thrown by docopt, results in usage message
        print(error, file=sys.stderr)
        sys.exit(1)
    except SystemExit:
        # user exception, program aborted by user
        sys.exit(1)
    except Exception as error:
        # exception we did no expect, show python backtrace
        logger.log.error('Unexpected error: %s', error)
        raise
