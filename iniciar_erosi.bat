@echo off
cd /d %~dp0
python -m venv venv
call venv\Scripts\activate
pip install flask flask-cors
python app.py
pause
