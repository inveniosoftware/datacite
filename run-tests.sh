#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2015-2020 CERN.
# SPDX-License-Identifier: MIT

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

python -m sphinx.cmd.build -qnNW docs docs/_build/html
python -m pytest
python -m sphinx.cmd.build -qnNW -b doctest docs docs/_build/doctest
