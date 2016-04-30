
from unittest.mock import patch

from dbassembly.app import App
from dbassembly.exceptions import DBAssemblyError

from .conftest import raises


def test_app():
    app = App(None)
    assert repr(app)

@patch('dbassembly.app.App.process')
def test_app_process(mock_app):
    app = App({'<assembly>':'a', '<output>':'b'})
    result = app.process()
    mock_app.assert_called_once('a', 'b')

@raises(DBAssemblyError)
def test_parse_wrong_assembly(tmpdir):
    foopath = tmpdir.join('foo')
    foopath.write("<wrong/>")
    app = App({'<assembly>':foopath.strpath,
               '<output>': None})
    app.process()

def test_parse_correct_assembly(tmpdir):
    foopath = tmpdir.join('foo')
    foopath.write("<assembly xmlns='http://docbook.org/ns/docbook'/>")
    app = App({'<assembly>':foopath.strpath,
               '<output>': None})
    app.process()
