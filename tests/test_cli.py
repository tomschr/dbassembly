
from unittest.mock import patch

from dbassembly.cli import (main, main_app, parsecli)


def test_main():
    result = main(['--murx'])
    assert result == 1


@patch('dbassembly.cli.main')
def test_main_with_KeyboardInterrupt(mock_kb):
    # TODO: This needs some more thoughts
    mock_kb.side_effect = KeyboardInterrupt
    result = main([])
    assert result


@patch('dbassembly.app.App')
def test_main_app_with_OSError(mock_app, docoptdict):
    mock_app.side_effect = OSError
    result = main_app(docoptdict)
    assert result == 30