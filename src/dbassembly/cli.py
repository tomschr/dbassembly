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

import os
import sys

from docopt import DocoptExit
from docopt import docopt
from lxml.etree import XMLSyntaxError

from . import __proc__
from . import __version__
from .app import App
from .exceptions import MissingAttributeRessource
from .exceptions import NoAssemblyFileError
from .exceptions import NoStructure
from .logger import log
from .logger import setloglevel


def parsecli(argv=None):
    """Parse command line arguments with docopt

    :param list argv: Arguments to parse or None (=use `sys.argv`)
    :return: parsed arguments
    :rtype: :py:class:`docopt.Dict`
    """
    _doc = """
usage:
    dbassembly -h | --help
    dbassembly --version
    dbassembly [-v]... [options] [--] <assembly>

Global options:
    --version
        show program version
    -v  raise verbosity

Input options:
    -b <basedir> --basedir=<basedir>
        define base directory of processing
    -f <format> --format=<format>
        specifies target output format.
        Multiple output formats separated by ';' may be specified.
        For example, "pdf;expert" means output format is "pdf" OR
        "expert".
    -s <struct_id> --struct=<struct_id>
        specifies the xml:id of the structure to processed.
        (default: first found structure)
    -p <profile>, --profile=<profile>
        specifies a profiling attribut; <profile> has the syntax:
          attribute_name=attribute_value
        If you need more, separate them by semicolon, for example:
        -p "os=a;arch=x86"
    -o <output>, --output=<output>
        save "flat" DocBook document (default goes to stdout)

Output options:
    --pretty-print
        pretty-print realized document

Arguments:
    <assembly>
        DocBook 5 assembly file
    """
    cli = docopt(_doc,
                 help=True,
                 version='%s version %s' % (__proc__, __version__),
                 # options_first=True,
                 argv=argv,
                 )
    return cli


def basename(path):
    """Returns basename of current path

    :param str path: path
    :return: relative path

    """
    return os.path.basename(path)


def main_app(cli):
    """Main entry point for testing purpose

    :param dict cli: dictionary from docopt parsing
    :return: success code (0 => ok; !=0 => error)
    """
    try:
        app = App(cli)
        return app.process()
    # except KeyboardInterrupt:  # pragma: nocover
    #    logger.log.error('%s aborted by keyboard interrupt' % __proc__)
    #    return 1
    except (MissingAttributeRessource, NoStructure) as error:
        log.error(error)
        # print(error, file=sys.stderr)
        return 10
    except (OSError, ) as error:
        log.error(error)
        return 20
    except (NoAssemblyFileError, XMLSyntaxError) as error:
        # log.error(error)
        log.error("%s\n"
                  "Reason: Probably %r is not an assembly file."
                  "" % (error, basename(cli['<assembly>']))
                  )
        return 30
    return 0


def main(argv=None):
    """Main entry point

    :param list argv: Arguments to parse or None (=use `sys.argv`)
    :return: result from :func:`App.process`
    """
    # argv = argv if argv else sys.argv

    try:
        cli = parsecli(argv)
    except DocoptExit as error:
        # exception thrown by docopt, results in usage message
        print(error, file=sys.stderr)
        return 1

    setloglevel(cli['-v'])
    log.debug("CLI result: %s", cli)
    return main_app(cli)
