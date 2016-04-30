
from unittest.mock import patch

from dbassembly.app import App


# from mock import patch

def test_app():
    app = App(None)
    assert repr(app)

@patch('dbassembly.app.App.process')
def test_app_process(mock_app):
    app = App({'<assembly>':'a', '<output>':'b'})
    result = app.process()
    mock_app.assert_called_once('a', 'b')
