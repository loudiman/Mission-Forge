@echo off

echo Installing Mission-Forge...

where python >nul 2>&1
if errorlevel 1 (
    echo Error: python not found. Install it from https://python.org
    exit /b 1
)

where pip >nul 2>&1
if errorlevel 1 (
    echo Error: pip not found. Install it from https://python.org
    exit /b 1
)

where npx >nul 2>&1
if errorlevel 1 (
    echo Error: npx not found. Install Node.js 18+ from https://nodejs.org
    exit /b 1
)

pip install git+https://github.com/loudiman/Mission-Forge.git && npx -y skills add loudiman/Mission-Forge

if errorlevel 1 exit /b 1

echo. & echo [OK] missionforge CLI installed
echo [OK] Agent skills installed
echo Run "missionforge init MF-001" to create your first mission.
