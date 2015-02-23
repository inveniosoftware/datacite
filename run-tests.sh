# This file is part of DataCite.
#
# Copyright (C) 2015 CERN.
#
# DataCite is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for
# more details.

pep257 datacite
sphinx-build -qnNW docs docs/_build/html
python setup.py test
