
from dbassembly.core import ASSEMBLY_TAG
from dbassembly.core import NS
from dbassembly.core import db


def test_db():
    tag = db('foo')
    assert tag == '{{{}}}foo'.format(NS['db'])

def test_assembly_tag():
    assembly = '{{{}}}assembly'.format(NS['db'])
    assert assembly == str(ASSEMBLY_TAG)
