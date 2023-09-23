#!/bin/bash



# Compile requirements/requirements for ai_driver
cd ./ai_driver
pip-compile requirements/requirements.in
pip-compile requirements/requirements-server.in
pip-compile requirements/requirements-dev.in
pip-compile requirements/requirements-test.in
pip-compile requirements/requirements-ui.in
echo "Pin update complete."
cd ..
