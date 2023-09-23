#! /usr/bin/env bash

# Run migrations
alembic upgrade head

# Create initial data in DB
python3.11 ./ai_driver/server/scripts/initial_data.py

# Let the DB start
python3.11 ./ai_driver/server/scripts/backend_pre_start.py
