#!/usr/bin/env bash

rm dist -rf
python3 setup.py sdist bdist_wheel
python3 -m twine upload  dist/* --verbose