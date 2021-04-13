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

The datacite package implements a Python client for DataCite MDS API and DataCite REST API.
You can find below full usage example of the DataCite MDS client API wrapper. Please see
the `DataCite MDS API documentation <https://support.datacite.org/docs/mds-api-guide>`_
for further information.

.. literalinclude:: ../tests/example/full.py
   :language: python
   :linenos:

You can find below an usage example of the DataCite REST client API wrapper. Please see
the `DataCite REST API documentation <https://support.datacite.org/docs/api>`_
for further information.

.. literalinclude:: ../tests/example/full_rest.py
   :language: python
   :linenos:

Please see the `DataCite Testing guide <https://support.datacite.org/docs/testing-guide>`_ to
know how to test this client with your test credentials.

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

DataCite v4.1 XML generation
============================

.. automodule:: datacite.schema41
   :members: dump_etree, tostring, validate

DataCite v4.2 XML generation
============================

.. automodule:: datacite.schema42
   :members: dump_etree, tostring, validate

.. include:: ../CHANGES.rst

.. include:: ../CONTRIBUTING.rst

License
=======

.. include:: ../LICENSE

.. note::

    In applying this license, CERN does not waive the privileges and immunities
    granted to it by virtue of its status as an Intergovernmental Organization
    or submit itself to any jurisdiction.

.. include:: ../AUTHORS.rst
