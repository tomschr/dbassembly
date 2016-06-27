#
# Copyright (c) 2016 SUSE Linux GmbH.  All rights reserved.
#
# This file is part of dbassembly.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

from functools import wraps
import pytest
from py.path import local

from dbassembly.core import NSMAP
from dbassembly.cli import parsecli


class raises(object): # pragma: no cover
    """
    exception decorator as used in nose, tools/nontrivial.py
    """
    def __init__(self, *exceptions):
        self.exceptions = exceptions
        self.valid = ' or '.join([e.__name__ for e in exceptions])

    def __call__(self, func):
        name = func.__name__

        def newfunc(*args, **kw):
            try:
                func(*args, **kw)
            except self.exceptions:
                pass
            except:
                raise
            else:
                message = "%s() did not raise %s" % (name, self.valid)
                raise AssertionError(message)
        newfunc = wraps(func)(newfunc)
        return newfunc


def xmldump(tree, indent=2):
    """Dump XML tree into hierarchical string

    :param element: ElementTree or Element
    :return: generator, yields strings
    """
    for i, elem in enumerate(tree.iter()):
        indstr=indent*" "
        if elem.text is None or (not elem.text.strip()):
            text = 'None'
        else:
            text = repr(elem.text.strip())
        yield i*indstr + "%s = %s" % (elem.tag, text)

        for attr in sorted(elem.attrib):
            yield (i+1)*indstr+"* %s = %r" % (attr, elem.attrib[attr])


# ------------------------------------------------------
# Fixtures
#

@pytest.fixture
def assembly(tmpdir):
    """Fixture: creates a file 'assembly.xml' in a temporary
       directory with an empty DocBook5 root element '<assembly>'.

       :return: Assembly file
       :rtype: :py:class:'py.path.local'
    """
    content="""<assembly xmlns={dbns!r}>
   <title>Test Assembly</title>
  <resources>
    <resource href="urn:x-pytest:foo" xml:id="topic1"/>
  </resources>

  <structure xml:id="result-topic1" resourceref="topic1"/>
</assembly>
    """
    xmlfile = tmpdir.join('assembly.xml')
    xmlfile.write(content.format(dbns=NSMAP['db']))
    return xmlfile


@pytest.fixture
def docoptdict():
    """Fixture: creates a faked dictionary object from docopt.

       :return: dictionary
       :rtype: dict
    """
    return parsecli(['foo.xml'])

# ------------------------------------------------------
# General
#
# http://pytest.org/latest/parametrize.html#basic-pytest-generate-tests-example

def casesdir():
    """Fixture: returns the "cases" directory relative to
       'conftest.py'

       :return: directory pointing to 'cases'
       :rtype: :py:class:'py.path.local'
    """
    return local(__file__).dirpath() / "cases"


def structdir():
    """Fixture: returns the "cases" directory relative to
       'conftest.py'

       :return: directory pointing to 'cases'
       :rtype: :py:class:'py.path.local'
    """
    return local(__file__).dirpath() / "struct"


def get_test_cases(testcasesdir,
                   casesxml='.case.xml',
                   patternout='.out.xml',
                   patternerr='.err.xml'):
    """Generator: yield name tuple of (casexmlfile, outputfile, errorfile)

       :param str casesxml: file extension of XML case file
       :param str patternout: file extension of output file
       :param str patternerr: file extension of error file
    """
    for case in testcasesdir:
        b = case.basename
        out = b.replace(casesxml, patternout)
        err = b.replace(casesxml, patternerr)
        out = case.new(basename=out)
        err = case.new(basename=err)
        yield (case, out, err)


def xmltestcase(metafunc, cases):
    """Compares .cases.xml files with .out.xml / .err.xml files

    HINT: The out file has to be an *exact* output. Each spaces
          is considered to be significant.
    """
    testcases = cases.listdir('*.case.xml', sort=True)

    # Create tuple of (original, outputfile, errorfile)
    result = get_test_cases(testcases)

    ids=[i.basename for i in testcases]
    metafunc.parametrize("xmltestcase", result, ids=ids)


def xmlteststruct(metafunc, struct):
    """Compares .cases.xml files with .struct.xml / .err.xml files
    """
    # cases = local(__file__).dirpath() / "cases"
    testcases = struct.listdir('*.case.xml', sort=True)

    # Create tuple of (original, outputfile, errorfile)
    result = get_test_cases(testcases, patternout='.out.struct')

    ids=[i.basename for i in testcases]
    metafunc.parametrize("xmlteststruct", result, ids=ids)


def pytest_generate_tests(metafunc):
    """Generate testcases for all *.case.xml files.
    """
    funcdict = dict(xmltestcase=[xmltestcase, casesdir()],
                    xmlteststruct=[xmlteststruct, structdir()],
                    )

    if not metafunc.fixturenames:
        return
    func, subdir = funcdict.get(metafunc.fixturenames[0], [None, None])
    if func is not None:
        func(metafunc, subdir)
