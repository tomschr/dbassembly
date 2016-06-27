
from unittest.mock import patch, MagicMock

from dbassembly.app import App
from io import StringIO
import pytest

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


@pytest.mark.parametrize("exp_exception", [
    OSError, # PermissionError, FileExistsError
])
@patch('builtins.open')
def test_app_raise_OSError(mock_open, exp_exception):
    with pytest.raises(exp_exception):
        mock_open.side_effect = exp_exception
        app = App({'<assembly>':'a', '--output': mock_open})
        app.process = MagicMock(side_effect=exp_exception)
        app.process()


@pytest.mark.parametrize("exp_exception", [
    OSError, PermissionError, FileExistsError, FileNotFoundError,
])
def test_app_raise_OSError_1(exp_exception):
    with pytest.raises(exp_exception):
        with patch.object(App, '__init__',
                      side_effect=exp_exception) as mock_app:
            app = App({'<assembly>':'a', '--output': 'foo.out'})
            app.process()
