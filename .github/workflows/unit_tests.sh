#!/bin/bash
set -e
TEST_DIR="tests"

echo "Running unit tests... "
pytest --junitxml=test-results/results.xml $TEST_DIR
echo "All tests passed!"
