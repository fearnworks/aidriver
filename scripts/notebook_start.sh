#!/bin/bash

# Check if /opt/venv exists and activate it
if [ -d "/opt/venv/bin" ]; then
  echo "Activating virtual environment..."
  source /opt/venv/bin/activate
  pip install /code
  # Add the virtual environment as a Jupyter kernel
  python -m ipykernel install --user --name=venv
fi

# Start Jupyter Lab without a password or token
exec "$@" --NotebookApp.token='' --NotebookApp.password=''
