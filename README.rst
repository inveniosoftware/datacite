==========
 DataCite
==========

.. image:: https://img.shields.io/travis/inveniosoftware/datacite.svg
   :target: https://travis-ci.org/inveniosoftware/datacite

.. image:: https://img.shields.io/coveralls/inveniosoftware/datacite.svg
   :target: https://coveralls.io/r/inveniosoftware/datacite?branch=master

.. image:: https://img.shields.io/pypi/v/datacite.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/datacite/

.. image:: https://img.shields.io/pypi/dm/datacite.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/datacite/

.. image:: https://img.shields.io/github/license/inveniosoftware/datacite.svg
   :target: https://github.com/inveniosoftware/datacite/blob/master/LICENSE

.. image:: https://img.shields.io/github/tag/inveniosoftware/datacite.svg
   :target: https://github.com/inveniosoftware/datacite/releases/




About
=====

Python API wrapper for the DataCite Metadata Store API and DataCite XML
generation.


Installation
============
The datacite package is on PyPI so all you need is: ::

    pip install datacite


Documentation
=============

Documentation is readable at http://datacite.readthedocs.io/ or can be
built using Sphinx: ::

    pip install datacite[docs]
    python setup.py build_sphinx


Testing
=======
Running the test suite is as simple as: ::

    pip install -e .[all]
    ./run-tests.sh
