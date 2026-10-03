@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
cd backend
uvicorn main:app --reload
