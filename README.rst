========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/dbassembly/badge/?style=flat
    :target: https://readthedocs.org/projects/dbassembly
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/tomschr/dbassembly.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tomschr/dbassembly

.. |requires| image:: https://requires.io/github/tomschr/dbassembly/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/tomschr/dbassembly/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/tomschr/dbassembly/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/tomschr/dbassembly

.. |codecov| image:: https://codecov.io/github/tomschr/dbassembly/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/tomschr/dbassembly

.. |landscape| image:: https://landscape.io/github/tomschr/dbassembly/master/landscape.svg?style=flat
    :target: https://landscape.io/github/tomschr/dbassembly/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/dbassembly.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/dbassembly

.. |downloads| image:: https://img.shields.io/pypi/dm/dbassembly.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/dbassembly

.. |wheel| image:: https://img.shields.io/pypi/wheel/dbassembly.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/dbassembly

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/dbassembly.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/dbassembly

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/dbassembly.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/dbassembly

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/tomschr/dbassembly/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/tomschr/dbassembly/


.. end-badges

Manage DocBook Assemblies

* Free software: BSD license

Installation
============

::

    pip install dbassembly

Documentation
=============

https://dbassembly.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
