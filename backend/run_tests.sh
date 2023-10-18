#!/usr/bin/env bash
MAPPLY_DATABASE_URL="postgresql://mapply_testing:mapply_testing@localhost:5679/mapply_testing" \
    python -m pytest
