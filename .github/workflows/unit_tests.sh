# #!/bin/bash
# set -e
# TEST_DIR="tests"

# echo "Running unit tests..."
# pytest --junitxml=test-results/results.xml $TEST_DIR
# echo "All tests passed!"
#!/bin/bash
set -e
TEST_DIR="tests"

echo "Current working directory: $(pwd)"

cd "$(dirname "$0")/../../"

if [ ! -f "./presets.json" ]; then
    echo "Error: presets.json not found!"
    exit 1
fi

echo "Running unit tests..."
pytest --junitxml=test-results/results.xml $TEST_DIR
echo "All tests passed!"
