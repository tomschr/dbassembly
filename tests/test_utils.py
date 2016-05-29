
from lxml import etree
from lxml.etree import QName
from dbassembly.core import xmlattr
from dbassembly.utils import collect_ids


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
