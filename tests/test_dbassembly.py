#
#
from io import StringIO
from unittest.mock import patch

from lxml import etree
from py.path import local
from testfixtures import LogCapture

from dbassembly.app import loadassembly
from dbassembly.cli import main_app
from dbassembly.docbook import assembly
from dbassembly.exceptions import BaseAssemblyError
from dbassembly.logger import log

from .conftest import xmldump


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


def test_structures(xmlteststruct):
    """Runs a testcase from struct/. This is used if you are more interested in
       the structure than the real representation of the XML.
       The xmlteststruct argument contains a tuple with three items (for example):

       * local('foo.case.xml') is the assembly file
       * local('foo.out.struct') is a (possible) output file; the content is an
         indented structure which represents the XML file. The structure
         contains element names (including its namespace), element attributes,
         and the content. Nested structures are indented.
       * local('foo.err.xml') is a (possible) file which contains errors from
         logging.

    :param xmlteststruct: Contains tuple: (assemblyfile, outputfile, errorfile)
    :param tmpdir: temporary directory
    :param capsys: fixture to capture sys.stdout & sys.stderr
    """
    assemblyfile, outputfile, errorfile = xmlteststruct

    with LogCapture(names=(log.name,)) as ll:
        xml = loadassembly(str(assemblyfile))
        result = assembly(xml)
        resultlist = list(xmldump(result))

    outputerr = errorfile.readlines(cr=False) if errorfile.isfile() else ['']
    outputstruct = outputfile.readlines(cr=False) if outputfile.isfile() else ['']
    # Check for empty strings at the end and remove them
    if outputstruct[-1] == '':
        outputstruct.pop()
    if outputerr[-1] == '':
        outputerr.pop()

    logerror = []
    for l in ll.records:
        if l.levelname != 'ERROR': continue
        logerror.extend(l.getMessage().rstrip().split("\n"))

    assert outputerr == logerror
    assert outputstruct == resultlist


