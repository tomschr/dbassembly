
from unittest.mock import patch

from dbassembly.app import App
from dbassembly.exceptions import DBAssemblyError
from dbassembly.exceptions import NoAssemblyFileError

from .conftest import raises


def test_app():
    app = App(None)
    assert repr(app)

@patch('dbassembly.app.App.process')
def test_app_process(mock_app):
    app = App({'<assembly>':'a', '<output>':'b'})
    result = app.process()
    mock_app.assert_called_once('a', 'b')

@raises(NoAssemblyFileError)
def test_parse_wrong_assembly(tmpdir):
    foopath = tmpdir.join('foo')
    foopath.write("<wrong/>")
    app = App({'<assembly>':foopath.strpath,
               '<output>': None})
    app.process()

def test_parse_correct_assembly(assembly):
    app = App({'<assembly>': assembly.strpath,
               '<output>': None})
    app.process()

def test_exception():
    try:
        raise DBAssemblyError("foo")
    except DBAssemblyError as error:
        assert str(error) == 'foo'
