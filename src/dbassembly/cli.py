"""
dbassembly.cli Module
=====================

Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from :func:`__main__` later, but that
  will cause problems: the code will get executed twice:

  - When you run :command:`python -mdbassembly` Python will execute
    :file:`__main__.py` as a script. That means there won't be any
    :func:`dbassembly.__main__` in :py:class:`sys.modules`.
  - When you import __main__ it will get executed again (as a module) because
    there's no :func:`dbassembly.__main__` in :py:class:`sys.modules`.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

from . import __version__

import argparse



def main(args=None):
    """Parse command line arguments

    :param list args: Arguments to parse or None (=use `sys.argv`)
    :return: parsed arguments
    :rtype: :py:class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description='Command description.')
    parser.add_argument('--version',
                        action='version',
                        version="%(prog)s {}".format(__version__),
                        )
    parser.add_argument('names',
                        metavar='NAME',
                        nargs=argparse.ZERO_OR_MORE,
                        help="A name of something.")
    args = parser.parse_args(args=args)
    print(args.names)
