
from unittest.mock import patch

from dbassembly.cli import main
from dbassembly.cli import parsecli

from .conftest import raises


def test_main():
    result = main(['--murx'])
    assert result == 1


@patch('dbassembly.cli.main')
def test_main_with_KeyboardInterrupt(mock_kb):
    # TODO: This needs some more thoughts
    mock_kb.side_effect = KeyboardInterrupt
    result = main([])
    assert result
