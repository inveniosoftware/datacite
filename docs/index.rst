============
 DataCite
============
.. currentmodule:: datacite

.. raw:: html

    <p style="height:22px; margin:0 0 0 2em; float:right">
        <a href="https://travis-ci.org/inveniosoftware/datacite">
            <img src="https://img.shields.io/travis/inveniosoftware/datacite.svg"
                 alt="travis-ci badge"/>
        </a>
        <a href="https://coveralls.io/r/inveniosoftware/datacite">
            <img src="https://img.shields.io/coveralls/inveniosoftware/datacite.svg"
                 alt="coveralls.io badge"/>
        </a>
    </p>

Python API wrapper for the DataCite Metadata Store API and DataCite XML generation.

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


Metadata Store API
===================

.. automodule:: datacite
   :members:

Errors
------

.. automodule:: datacite.errors
   :members:

DataCite v3.1 XML generation
============================

.. automodule:: datacite.schema31
   :members: dump_etree, tostring, validate

DataCite v4.0 XML generation
============================

.. automodule:: datacite.schema40
   :members: dump_etree, tostring, validate

.. include:: ../CHANGES.rst

.. include:: ../CONTRIBUTING.rst

License
=======

.. include:: ../LICENSE

.. include:: ../AUTHORS.rst
