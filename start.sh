#!/bin/bash

# initialize folders
mkdir -p data
mkdir -p data/cache
mkdir -p data/db
mkdir -p .streamlit

# initialize files
touch data/db/local.db
touch .streamlit/config.toml
touch .streamlit/secrets.toml

# initialize venv
python -m venv .venv
pip install -r requirements.txt
source .venv/bin/activate

# start streamlit
streamlit run main.py >> log.txt