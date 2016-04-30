=================
dbassembly Usage
=================

.. |tdg_assemblies| replace:: http://docbook.org/tdg51/en/html/ch06.html
.. |tdg_ref| replace:: http://docbook.org/tdg51/en/html/assembly.html

NAME
----

dbassembly-Managing DocBook assemblies.


SYNOPSIS
--------

.. program-output:: bash -c "dbassembly 2>&1 | sed -e '1d;s/^[ ]*//g'"
    :returncode: 0


DESCRIPTION
-----------

*DocBook assemblies* are XML files based on the DocBook 5.1 schema.

*Topics* are independant units of documentation. They are collected,
grouped and organized together to form an output deliverable. In order
to make such documentation, the structure is definied in the assembly
file.

Each assembly file contains the ``<assembly>`` root element, the
different topics as modules, and the structure where the topics are
organized.

The script :command:`dbassembly` collects all the modules, applies any
rules to it, and creates a flat output file, called the *realized document*.
This document can be feed into the DocBook stylesheets to create an output
deliverable.


EXAMPLE
-------

TBD


FILES
-----

TBD

SEE ALSO
--------

* |github_url|
  Project homepage
* |tdg_assemblies|
  Describes DocBook assemblies, introduced in version 5.1
* |tdg_ref|
  Reference of ``assembly`` element

AUTHOR
------

|author| |author_email|
