#
from dbassembly.cli import main_app
from dbassembly.exceptions import BaseAssemblyError
from dbassembly.logger import log

#
from io import StringIO
from lxml import etree
from py.path import local
from testfixtures import LogCapture
from unittest.mock import patch


def test_cases(xmltestcase):
    """Runs one testcase from cases/

    :param xmltestcase: Contains tuple: (original, outputfile, errorfile)
    :param tmpdir: temporary directory
    :param capsys: fixture to capture sys.stdout & sys.stderr
    """
    original, outputfile, errorfile = xmltestcase

    with patch('dbassembly.app.sys.stdout', new=StringIO()) as mock_sys:
        with LogCapture(names=(log.name,)) as ll:
            result = main_app({'<assembly>': str(original),
                               '<output>': None})

    outputerr = errorfile.read().rstrip() if errorfile.isfile() else ""
    outputxml = outputfile.read().rstrip() if outputfile.isfile() else ""

    assert outputerr == "\n".join([l.getMessage() for l in ll.records
                             if l.levelname == 'ERROR'])
    assert outputxml == mock_sys.getvalue()
