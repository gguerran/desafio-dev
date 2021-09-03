#!/bin/sh

flake8 . --extend-exclude=dist,build,static,migrations,venv --max-line-length 119
