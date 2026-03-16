@echo off
echo Starting AI Events Europe Collector: Daily Enrichment Pass...
cd /d %~dp0
python agent.py
echo.
echo Process finished. Check the dashboard at http://127.0.0.1:5000
pause
