============
 DataCite
============
.. currentmodule:: datacite

.. raw:: html

    <p style="height:22px; margin:0 0 0 2em; float:right">
        <a href="https://travis-ci.org/inveniosoftware/datacite">
            <img src="https://travis-ci.org/inveniosoftware/datacite.png?branch=master"
                 alt="travis-ci badge"/>
        </a>
        <a href="https://coveralls.io/r/inveniosoftware/datacite">
            <img src="https://coveralls.io/repos/inveniosoftware/datacite/badge.png?branch=master"
                 alt="coveralls.io badge"/>
        </a>
    </p>

Python API wrapper for the DataCite Metadata Store API.

Installation
============

The datacite package is on PyPI so all you need is:

.. code-block:: console

    $ pip install datacite


Usage
=====

Below is full usage example of the DataCite MDS client API wrapper. Please see
the `DataCite MDS API documentation <https://mds.datacite.org/static/apidoc>`_
for further information on the API.

.. literalinclude:: ../tests/example/full.py
   :language: python
   :linenos:


API
===

.. automodule:: datacite
   :members:

Errors
------

.. automodule:: datacite.errors
   :members:

.. include:: ../CHANGES.rst

.. include:: ../CONTRIBUTING.rst

License
=======

.. include:: ../LICENSE

.. include:: ../AUTHORS.rst
