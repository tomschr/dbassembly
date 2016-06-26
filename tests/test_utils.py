
from dbassembly.utils import collect_ids, isXMLSpace, isXMLChar

from lxml import etree
from lxml.etree import QName

import pytest


def setup_module(module):
    """ module setup; introduces 'xml' and 'result'
        as variables
    """
    module.xml = etree.fromstring("""<assembly
        xml:id="start"
        xmlns="http://docbook.org/ns/docbook">
  <resources>
    <resource href="data/topic1.xml" xml:id="topic1"/>
    <resource href="data/topic2.xml" xml:id="topic2"/>
    <resource href="data/topic3.xml" xml:id="topic3"/>
  </resources>

</assembly>
        """)
    module.result = collect_ids(xml)


def test_collect_ids_xmlids():
    """Tests all xml:id's """
    assert {'start', 'topic3', 'topic1', 'topic2'} == set(result)


def test_collect_ids_localnames():
    """Tests all names"""
    assert {'assembly', 'resource'} == {QName(result[i]).localname
                                        for i in result}


def test_collect_ids_hrefs():
    """Tests all href attributes"""
    assert {None, 'data/topic2.xml',
            'data/topic1.xml', 'data/topic3.xml'} == { result[i].attrib.get('href') for i in result }


@pytest.mark.parametrize('char,result', [
    (' ',  True),
    ('\t', True),
    ('\n', True),
    ('\r', True),
    ('a',  False),
    ('\u20ac', False),
])
def test_isXMLSpace(char, result):
    assert isXMLSpace(char) == result


@pytest.mark.parametrize('char,result', [
    ('\t', True),
    ('\n', True),
    ('\r', True),
    # [#x20-#xD7FF]
    (' ',       True),
    ('\uA001',  True),
    ('\uD7FF',  True),
    # [#xE000-#xFFFD]
    ('\uE000',  True),
    ('\uEFFE',  True),
    ('\uFFFD',  True),
    # [#x10000-#x10FFFF]
    ('\U00010000', True),
    ('\U0008FFFF', True),
    ('\U0010FFFF', True),
])
def test_isXMLChar(char, result):
    assert isXMLChar(char) == result
