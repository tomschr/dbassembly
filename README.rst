========
Overview
========

.. start-badges

|travis| |landscape| |codecov| |scrutinizer| |requires|

.. sidebar:: Work in Progress

    This project is work in progress (planning state)

.. .. |docs| image:: https://readthedocs.org/projects/dbassembly/badge/?style=flat
    :target: https://readthedocs.org/projects/dbassembly
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/tomschr/dbassembly.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tomschr/dbassembly

.. |requires| image:: https://requires.io/github/tomschr/dbassembly/requirements.svg?branch=master
     :target: https://requires.io/github/tomschr/dbassembly/requirements/?branch=master
     :alt: Requirements Status

.. |codecov| image:: https://codecov.io/github/tomschr/dbassembly/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/tomschr/dbassembly

.. |landscape| image:: https://landscape.io/github/tomschr/dbassembly/master/landscape.svg?style=flat
    :target: https://landscape.io/github/tomschr/dbassembly/master
    :alt: Code Quality Status

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/tomschr/dbassembly/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/tomschr/dbassembly/

.. end-badges

Manage DocBook Assemblies

* Free software: GPL license


Installation
============

::

    pip install dbassembly


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
