
from dbassembly.core import ASSEMBLY_TAG
from dbassembly.core import NSMAP
from dbassembly.core import db


def test_db():
    tag = db('foo')
    assert tag == '{{{}}}foo'.format(NSMAP['db'])

def test_assembly_tag():
    assembly = '{{{}}}assembly'.format(NSMAP['db'])
    assert assembly == str(ASSEMBLY_TAG)
