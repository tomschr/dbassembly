#
#
from io import StringIO
from unittest.mock import patch
import logging

from lxml import etree
from py.path import local
from testfixtures import LogCapture

from dbassembly.app import loadassembly
from dbassembly.cli import main_app
from dbassembly.assembly import assembly
from dbassembly.exceptions import BaseAssemblyError

from .conftest import xmldump

log = logging.getLogger('dbassembly')


def test_cases(xmltestcase):
    """Runs a testcase from cases/. This is used if you need an *exact*
       comparison between real output and expected output.
       The xmltestcase argument contains a tuple with three items (for example):

       * local('foo.case.xml') is the assembly file
       * local('foo.out.xml') is a (possible) output file; the content has to
         be an *exact* output.
       * local('foo.err.xml') is a (possible) file which contains errors from
         logging.

    :param xmltestcase: Contains tuple: (assembly, outputfile, errorfile)
    :param tmpdir: temporary directory
    :param capsys: fixture to capture sys.stdout & sys.stderr
    """
    assemblyfile, outputfile, errorfile = xmltestcase

    with patch('dbassembly.app.sys.stdout', new=StringIO()) as mock_sys:
        with LogCapture(names=(log.name,)) as ll:
            result = main_app({'<assembly>': str(assemblyfile),
                               '--output': None})

    outputerr = errorfile.readlines(cr=False) if errorfile.isfile() else ['']
    outputxml = outputfile.read().rstrip() if outputfile.isfile() else ""
    # Check for empty strings at the end and remove them
    if outputerr[-1] == '':
        outputerr.pop()

    logerror = []
    for l in ll.records:
        if l.levelname != 'ERROR': continue
        logerror.extend(l.getMessage().rstrip().split("\n"))

    assert outputerr == logerror
    assert outputxml == mock_sys.getvalue()
