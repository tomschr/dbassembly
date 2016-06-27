#
from dbassembly.checker import iterxmlid

from lxml import etree
from unittest.mock import patch, MagicMock
import pytest


@pytest.mark.parametrize('xmlstr,expected', [
    ('<root/>', 0),
    ('<root xml:id="r"/>', 1),
    ('<root xmlns="urn:x-test" xml:id="ff"/>', 1),
    ('<root xml:id="foo"><a/><b xml:id="b"/></root>', 2),
    ('<root xml:id="foo"><a xml:id="a"/><b/></root>', 2),

])
def test_checker_iterxmlid(xmlstr, expected):
    xml = etree.XML(xmlstr)
    assert len(list(iterxmlid(xml))) == expected
