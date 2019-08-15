==========
 DataCite
==========

.. image:: https://github.com/inveniosoftware/datacite/workflows/CI/badge.svg
        :target: https://github.com/inveniosoftware/datacite/actions

.. image:: https://img.shields.io/coveralls/inveniosoftware/datacite.svg
   :target: https://coveralls.io/r/inveniosoftware/datacite?branch=master

.. image:: https://img.shields.io/pypi/v/datacite.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/datacite/

.. image:: https://pepy.tech/badge/datacite?maxAge=2592000
   :target: https://pypi.python.org/pypi/datacite/

.. image:: https://img.shields.io/pypi/l/datacite.svg
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

If you're using zsh, use this pip command instead:

    pip install -e .'[all]'

Some tests require a DataCite Test Account.  
Set the following environment variables 
$DATACITE_USER, $DATACITE_PW, $DATACITE_PREFIX 
with your account information for doi.test.datacite.org and
run: ::

    ./run-tests-pw.sh
