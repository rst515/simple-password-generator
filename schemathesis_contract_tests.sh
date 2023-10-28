#!/bin/bash
# Script to run the required schemathesis tests, allowing for specific handling of different endpoints
# Requires the BASE_URL as the only positional argument

BASE_URL=$1
echo "Running Schemathesis API Contract Tests for: SimplePasswordGet"
if schemathesis run -E /simple_password -b "$BASE_URL" api-contract.yaml -v --hypothesis-max-examples=1 --workers auto --cassette-path simple_password.yaml --show-errors-tracebacks --checks all;
then
  echo "SimplePasswordGet Success"
else
  exit
fi
