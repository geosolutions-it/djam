#!/usr/bin/env bash

virtualenv --no-site-packages -p /usr/bin/python3 venv_test
source venv_test/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests and fail if coverage below 80%
cd project
./run_tests.sh
coverage report --fail-under=80
cd -

# Add black tests

deactivate
rm -rf venv_test
