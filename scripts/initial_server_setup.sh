#!/bin/bash

DOWNLOAD_MODEL=true
INIT_VECTORSTORE=true

while getopts "adv" opt; do
  case ${opt} in
    a )
      DOWNLOAD_MODEL=true
      INIT_VECTORSTORE=true
      ;;
    d )
      DOWNLOAD_MODEL=false
      ;;
    v )
      INIT_VECTORSTORE=false
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument." 1>&2
      exit 1
      ;;
  esac
done

sudo docker network create dd-network # handle for folks who don't have docker groups set up

python3.10 -m venv .server_venv && source .server_venv/bin/activate
python3.10 -m pip install --upgrade pip
python3.10 -m pip install -r ./ai_driver/requirements/requirements.txt

if [ "$DOWNLOAD_MODEL" = true ]; then
  python3.10 ./ai_driver/ai_driver/scripts/download_model.py
fi

if [ "$INIT_VECTORSTORE" = true ]; then
  python3.10 ./scripts/init_local_vectorstore.py
fi
