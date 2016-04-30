
from unittest.mock import patch

from dbassembly.cli import main
from dbassembly.cli import parsecli

from .conftest import raises


@raises(SystemExit)
def test_main():
    main(['--murx'])

@raises(SystemExit)
@patch('dbassembly.cli.main')
def test_main_with_KeyboardInterrupt(mock_kb):
    mock_kb.side_effect = KeyboardInterrupt
    main([])

def test_main_with_assembly_file():
    assembly = 'assembly.xml'
    cli = parsecli([assembly])
    assert cli['<assembly>'] == assembly

def test_main_with_assembly_and_output_file():
    assembly = 'assembly.xml'
    output = 'output.xml'
    cli = parsecli([assembly, output])
    assert cli['<assembly>'] == assembly
    assert cli['<output>'] == output

