#!/bin/bash

set -e

echo "Running migrations..."
poetry run alembic upgrade head

echo "Running tests..."
poetry run tests

echo "Starting app..."
poetry run start