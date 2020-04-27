#!/usr/bin/env bash

python -m venv venv_test
source venv_test/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Bandit Security Check, only fails on medium or above

bandit -ll -r project

# Run tests and fail if coverage below 80%
cd project
./run_tests.sh
coverage report --fail-under=80
cd -

# Add black tests
black --check project/

deactivate
rm -rf venv_test
