#!/bin/bash

# Download the dataset
curl "https://www.kaggle.com/datasets/hadasu92/cnn-articles-after-basic-cleaning#:~:text=Download%20(-,92,-MB)"

# Unzip the dataset
unzip archive.zip -d .

# Run the extract_keywords function
python -c 'from app.services.text_analysis import extract_keywords; extract_keywords()'

# Start the FastAPI service
poetry run uvicorn main:app --host 0.0.0.0 --port 8000