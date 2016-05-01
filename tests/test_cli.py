
from unittest.mock import patch

from dbassembly.cli import main
from dbassembly.cli import parsecli

from .conftest import raises


def test_main():
    result = main(['--murx'])
    assert result == 1


@patch('dbassembly.cli.main')
def test_main_with_KeyboardInterrupt(mock_kb):
    mock_kb.side_effect = KeyboardInterrupt
    result = main([])
    assert result == 1

def test_main_with_assembly_file(assembly):
    result = main([assembly.strpath])
    assert result == 0

def test_main_with_assembly_and_output_file(assembly):
    tmpdir = assembly.dirpath()
    output = tmpdir.join('output.xml')
    result = main([assembly.strpath, output.strpath])
    assert result == 0
