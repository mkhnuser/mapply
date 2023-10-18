#!/usr/bin/env bash
MAPPLY_DATABASE_URL="postgresql://mapply:mapply@localhost:5678/mapply" \
    python -m logic.app
