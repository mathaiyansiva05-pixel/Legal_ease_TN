@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
cd frontend
streamlit run app.py
