#!/bin/bash

PROJECT_NAME="testing"

# Start Kafka
docker compose -p ${PROJECT_NAME} up kafka --wait

# Start service separately since it's defined in another compose file and
# doesn't know when Kafka is healthy.
docker compose -p ${PROJECT_NAME} up append-text-naive --wait --build

# Run the tests
docker compose -p ${PROJECT_NAME} run --build --rm tester

# Get the exit code of the tests - '0' indicates passing tests
TEST_RESULT=$?

# Stop the stack and cleanup
docker compose -p ${PROJECT_NAME} down --remove-orphans

# Exit with the same code as the test result
exit ${TEST_RESULT}
