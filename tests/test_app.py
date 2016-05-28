
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
    # mock_open.side_effect = func_open
    mock_exist.return_value = True
    app = App({'<assembly>':'a', '--output':'b'})
