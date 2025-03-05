@echo off
echo Finding and killing process using port 5054...

for /f "tokens=5" %%p in ('netstat -ano ^| findstr :5054') do (
    echo Killing process with PID %%p...
    taskkill /F /PID %%p
)

echo Done.
pause