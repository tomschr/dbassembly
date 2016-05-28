
from unittest.mock import patch

from dbassembly.app import App
from io import StringIO

from .conftest import raises


def test_app():
    app = App(None)
    assert repr(app)


@raises(FileExistsError)
@patch('dbassembly.app.os.path.exists')
def test_app_file_exists(mock_exist):
    mock_exist.return_value = True
    app = App({'<assembly>':'a', '--output':'b'})


@patch('dbassembly.app.os.path.exists')
@patch('builtins.open')
def test_app_create_file(mock_open, mock_exist):
    mock_exist.return_value = False
    mock_open.return_value = StringIO()
    app = App({'<assembly>':'a', '--output': mock_open})
