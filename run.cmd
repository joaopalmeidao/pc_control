@echo off
echo Starting backend...
start cmd /k "cd backend && call venv\Scripts\activate && python server.py"

echo Starting frontend...
start cmd /k "cd frontend && npm run dev"

echo Both frontend and backend are starting...