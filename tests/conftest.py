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

try:
    from dbassembly.core import NS
except ImportError:
    pass


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
    xmlfile.write(content.format(dbns=NS['db']))
    return xmlfile


# ------------------------------------------------------
# General
#
# http://pytest.org/latest/parametrize.html#basic-pytest-generate-tests-example
def pytest_generate_tests(metafunc):
    """Generate testcases for all *.case.xml files
    """
    cases = local(__file__).dirpath() / "cases"
    if 'xmltestcase' in metafunc.fixturenames:
        testcases = cases.listdir('*.case.xml', sort=True)

        # Create tuple of (original, outputfile, errorfile)
        result = []
        for case in testcases:
            b = case.basename
            out = b.replace('.case.xml', '.out.xml')
            err = b.replace('.case.xml', '.err.xml')
            out = case.new(basename=out)
            err = case.new(basename=err)
            result.append((case, out, err))

        ids=[i.basename for i in testcases]
        metafunc.parametrize("xmltestcase",
                             result,
                             ids=ids)
