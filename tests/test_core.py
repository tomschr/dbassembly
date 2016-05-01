
from dbassembly.core import ASSEMBLY_TAG
from dbassembly.core import NS
from dbassembly.core import db


def test_db():
    tag = db('foo')
    assert tag == '{{{}}}foo'.format(NS['DB'])

def test_assembly_tag():
    assembly = '{{{}}}assembly'.format(NS['DB'])
    assert assembly == str(ASSEMBLY_TAG)
