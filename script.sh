#!/bin/bash
cd frontend
npm install
cd ..
cd python_files
py -m venv venv
pip install -r requirements.txt
venv/scripts/activate
uvicorn api.main:app --reload && cd .. && cd frontend && npm start
